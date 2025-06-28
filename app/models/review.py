from sqlalchemy import Column, Integer, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.db_base import Base

class Review(Base):
    __tablename__ = "review"
    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("book.id"), index=True)
    review_text = Column(Text)
    rating = Column(Integer)
    book = relationship("Book", back_populates="reviews") 