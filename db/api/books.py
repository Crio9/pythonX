from fastapi import APIRouter, Depends

from schemas.books import CreateBookSchema, UpdateBookSchema, BookSchema
from services.books import BookService

router = APIRouter()

@router.post('/books')
def create_book(book: CreateBookSchema, service: BookService = Depends()):
    create_result = service.create_book(book)

    return {"message": "success", "data": create_result}


@router.get('/books')
def get_books_collection():
    pass


@router.get('/books/{id}')
def get_book():
    pass


@router.patch('/books/{id}')
def edit_book():
    pass


@router.delete('/books/{id}')
def delete_book():
    pass
