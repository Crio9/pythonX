from pydantic import BaseModel


class BookSchema(BaseModel):
    id: int
    name: str
    author: str
    description: str
    pages: int
    style: str
    isbn: str
    publisher: str


class CreateBookSchema(BaseModel):
    name: str
    author: str
    description: str
    pages: int
    style: str
    isbn: str
    publisher: str


class UpdateBookSchema(BaseModel):
    name: str
    author: str
    description: str