from fastapi import Depends
from repositories.books import BookRepository
from schemas.books import CreateBookSchema
from models.books import Book


class BookService:
    def __init__(self, repository: BookRepository = Depends()):
        self.repository = repository

    def create_book(self, book: CreateBookSchema) -> Book:
        create_result = self.repository.create(book)

        output = book.model_dump()
        output.update({
            "id": create_result.id,
        })

        return output

    def get_books_collection(self):
        pass

    def get_book(self):
        pass

    def edit_book(self):
        pass

    def delete_book(self):
        pass
