from http import HTTPStatus

from fastapi import HTTPException

from app.models.book import Book
from app.repositories.book_repository import get_by_title, save


def create_book_service(session, book_schema):
    db_book = get_by_title(session, book_schema.title)

    if db_book:
        if db_book.title == book_schema.title:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='Livro já possui registro',
            )

    book = Book(
        year=book_schema.year,
        title=book_schema.title,
    )

    save(session, book)
    session.commit()
    session.refresh(book)

    return book
