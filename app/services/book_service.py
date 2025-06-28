import logging

logging.basicConfig(level=logging.INFO)

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from app.models.book import Book
from app.models.review import Review
from app.schemas.book import BookCreate
from app.schemas.review import ReviewCreate
from fastapi import HTTPException
from app.cache.redis_cache import redis_cache

async def get_books_service(db: AsyncSession):
    cache_key = "books:list"
    try:
        cached = await redis_cache.get_json(cache_key)
        if cached:
            logging.info("[REDIS] Cache hit for books:list")
            return cached
        else:
            logging.info("[REDIS] Cache miss for books:list")
    except Exception as e:
        logging.warning(f"[REDIS] Unavailable: {e}. Falling back to DB.")
    logging.info("[DB] Fetching books from database.")
    result = await db.execute(
        select(Book).options(selectinload(Book.reviews))
    )
    books = result.scalars().all()
    
    books_with_reviews = []
    for book in books:
        books_with_reviews.append({
            "id": book.id,
            "title": book.title,
            "author": book.author,
            "reviews": [
                {"id": r.id, "review_text": r.review_text, "rating": r.rating, "book_id": r.book_id}
                for r in book.reviews
            ]
        })
    try:
        await redis_cache.set_json(cache_key, books_with_reviews)
        logging.info("[REDIS] Cache set for books:list")
    except Exception as e:
        logging.warning(f"[REDIS] Unavailable (set): {e}.")
    return books_with_reviews

async def create_book_service(db: AsyncSession, book: BookCreate):
    db_book = Book(**book.dict())
    db.add(db_book)
    await db.commit()
    await db.refresh(db_book)
    
    try:
        await redis_cache.redis.delete("books:list")
        logging.info("[REDIS] Cache invalidated for books:list after book creation")
    except Exception as e:
        logging.warning(f"[REDIS] Unavailable (delete books:list): {e}.")
    return db_book

async def get_book_reviews_service(db: AsyncSession, book_id: int):
    cache_key = f"book:{book_id}:reviews"
    try:
        cached = await redis_cache.get_json(cache_key)
        if cached:
            logging.info(f"[REDIS] Cache hit for {cache_key}")
            return cached
        else:
            logging.info(f"[REDIS] Cache miss for {cache_key}")
    except Exception as e:
        logging.warning(f"[REDIS] Unavailable: {e}. Falling back to DB.")
    
    book_result = await db.execute(select(Book).where(Book.id == book_id))
    book_obj = book_result.scalar_one_or_none()
    if not book_obj:
        raise HTTPException(status_code=404, detail="Book not found")
    
    review_result = await db.execute(select(Review).where(Review.book_id == book_id))
    reviews = review_result.scalars().all()
    if not reviews:
        raise HTTPException(status_code=404, detail=f"No reviews added for the Book - {book_id}")
    try:
        await redis_cache.set_json(cache_key, [
            {"id": r.id, "review_text": r.review_text, "rating": r.rating, "book_id": r.book_id}
            for r in reviews
        ])
        logging.info(f"[REDIS] Cache set for {cache_key}")
    except Exception as e:
        logging.warning(f"[REDIS] Unavailable (set {cache_key}): {e}.")
    return reviews

async def create_review_service(db: AsyncSession, book_id: int, review: ReviewCreate):
    book_result = await db.execute(select(Book).where(Book.id == book_id))
    book_obj = book_result.scalar_one_or_none()
    if not book_obj:
        raise HTTPException(status_code=404, detail="Book not found")
    db_review = Review(**review.dict(), book_id=book_id)
    db.add(db_review)
    await db.commit()
    await db.refresh(db_review)
    
    try:
        await redis_cache.redis.delete("books:list")
        await redis_cache.redis.delete(f"book:{book_id}:reviews")
        logging.info(f"[REDIS] Cache invalidated for books:list and book:{book_id}:reviews after review creation")
    except Exception as e:
        logging.warning(f"[REDIS] Unavailable (delete caches): {e}.")
    return db_review 