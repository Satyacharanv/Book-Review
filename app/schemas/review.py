from pydantic import BaseModel
from typing import Optional

class ReviewBase(BaseModel):
    review_text: Optional[str] = None
    rating: int

class ReviewCreate(ReviewBase):
    pass

class ReviewRead(ReviewBase):
    id: int
    book_id: int
    class Config:
        from_attributes = True 