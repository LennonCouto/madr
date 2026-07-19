from http import HTTPStatus

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_session
from app.schemas.book import BookPublic, BookSchema, BookUpdate, Message
from app.services.book_service import (
    create_book_service,
    delete_book_with_id_service,
    read_books,
    update_book_service,
)

router = APIRouter(prefix='/book', tags=['Book'])


@router.post('/', status_code=HTTPStatus.CREATED, response_model=BookPublic)
def create_book(book: BookSchema, session: Session = Depends(get_session)):
    return create_book_service(session, book)


@router.get('/{id_book}', status_code=HTTPStatus.OK, response_model=BookPublic)
def read_books_with_id(session: Session = Depends(get_session), id_book=int):
    return read_books(session, id_book)


@router.patch(
    '/{id_book}',
    status_code=HTTPStatus.OK,
    response_model=BookPublic,
)
def update_book(
    id_book: int,
    book: BookUpdate,
    session: Session = Depends(get_session),
):
    return update_book_service(session, book, id_book)


@router.delete('/{id_book}', status_code=HTTPStatus.OK, response_model=Message)
def delete_book(id_book: int, session: Session = Depends(get_session)):
    return delete_book_with_id_service(session, id_book)
