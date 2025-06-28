from pydantic import BaseModel
from typing import List, Optional
from app.schemas.review import ReviewRead

class BookBase(BaseModel):
    title: str
    author: str

class BookCreate(BookBase):
    pass

class BookRead(BookBase):
    id: int
    class Config:
        from_attributes = True

class BookWithReviews(BookRead):
    reviews: List[ReviewRead] = []
    class Config:
        from_attributes = True 