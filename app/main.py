from fastapi import FastAPI
from app.routes.books import router as books_router
from app.db import engine
from app.db_base import Base
from app.models import book, review

app = FastAPI(title="Book Review API")

app.include_router(books_router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Book Review API"}

@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
