from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.sql import func

from core.database import Base

class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    author = Column(String(255), nullable=False)
    description = Column(String(100), nullable=False)
    pages = Column(Integer, nullable=False)
    style = Column(String(255), nullable=False)
    isbn = Column(String(255), nullable=False)
    publisher = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())