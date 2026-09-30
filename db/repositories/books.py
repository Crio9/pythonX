from fastapi import Depends
from sqlalchemy.orm import Session

from core.database import get_db
from models.books import Book
from schemas.books import CreateBookSchema, UpdateBookSchema


class BookRepository:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def create(self, book: CreateBookSchema) -> Book:
        db_book = Book(**book.model_dump())
        self.db.add(db_book)
        self.db.commit()
        self.db.refresh(db_book)

        return db_book

