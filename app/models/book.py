from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db_base import Base

class Book(Base):
    __tablename__ = "book"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    reviews = relationship("Review", back_populates="book", cascade="all, delete-orphan") 