from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.session import get_session
from app.schemas.book import (
    BookCreate,
    BookPublic,
    BookList,
    BookUpdate,
    Filter,
    Message,
)
from app.services.book_service import (
    create_book_service,
    delete_book_with_id_service,
    read_books,
    update_book_service,
)

from app.repositories.book_repository import get_filter_book


router = APIRouter(prefix='/book', tags=['Book'])


@router.post('/', status_code=HTTPStatus.CREATED, response_model=BookPublic)
def create_book(book: BookCreate, session: Session = Depends(get_session)):
    return create_book_service(session, book)


@router.get('/', response_model=BookList)
def read_books_with_filter(
    book_filter: Annotated[Filter, Query()],
    session: Session = Depends(get_session),
):
    return get_filter_book(
        session, book_filter.title,
        book_filter.year, book_filter.offset, book_filter.limit
    )


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
