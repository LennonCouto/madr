from http import HTTPStatus

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_session
from app.schemas.book import BookPublic, BookSchema, BookUpdate
from app.services.book_service import (
    create_book_service,
    read_books,
    update_book_service,
)

router = APIRouter(prefix='/book', tags=['Book'])


@router.post('/', status_code=HTTPStatus.CREATED, response_model=BookPublic)
def create_book(book: BookSchema, session: Session = Depends(get_session)):
    return create_book_service(session, book)


@router.get('/{book_id}', status_code=HTTPStatus.OK, response_model=BookPublic)
def read_books_with_id(session: Session = Depends(get_session), book_id=int):
    return read_books(session, book_id)


@router.patch(
    '/{book.id}', status_code=HTTPStatus.OK, response_model=BookPublic
)
def update_book(
    book_id: int,
    book: BookUpdate,
    session: Session = Depends(get_session),
):
    return update_book_service(session, book, book_id)
