from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.schemas.book import BookCreate, BookRead, BookWithReviews
from app.schemas.review import ReviewCreate, ReviewRead
from app.services.book_service import (
    get_books_service, create_book_service, get_book_reviews_service, create_review_service
)
from app.db import SessionLocal

router = APIRouter(prefix="/books", tags=["Books"])

async def get_db():
    async with SessionLocal() as session:
        yield session

@router.get("/", response_model=List[BookWithReviews])
async def get_books(db: AsyncSession = Depends(get_db)):
    return await get_books_service(db)

@router.post("/", response_model=BookRead, status_code=status.HTTP_201_CREATED)
async def create_book(book: BookCreate, db: AsyncSession = Depends(get_db)):
    return await create_book_service(db, book)

@router.get("/{book_id}/reviews", response_model=List[ReviewRead])
async def get_book_reviews(book_id: int, db: AsyncSession = Depends(get_db)):
    return await get_book_reviews_service(db, book_id)

@router.post("/{book_id}/reviews", response_model=ReviewRead, status_code=status.HTTP_201_CREATED)
async def create_review(book_id: int, review: ReviewCreate, db: AsyncSession = Depends(get_db)):
    return await create_review_service(db, book_id, review) 