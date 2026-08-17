from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.repositories.book_repository import get_filter_book
from app.schemas.book import (
    BookCreate,
    BookList,
    BookPublic,
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

router = APIRouter(prefix='/book', tags=['Book'])


@router.post('/', status_code=HTTPStatus.CREATED, response_model=BookPublic)
async def create_book(
    book: BookCreate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    return await create_book_service(session, book)


@router.get('/', response_model=BookList)
async def read_books_with_filter(
    book_filter: Annotated[Filter, Query()],
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    return await get_filter_book(
        session,
        book_filter.title,
        book_filter.year,
        book_filter.offset,
        book_filter.limit,
    )


@router.get('/{id_book}', status_code=HTTPStatus.OK, response_model=BookPublic)
async def read_books_with_id(
    id_book=int,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    return await read_books(session, id_book)


@router.patch(
    '/{id_book}', status_code=HTTPStatus.OK, response_model=BookPublic
)
async def update_book(
    id_book: int,
    book: BookUpdate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    return await update_book_service(session, book, id_book)


@router.delete('/{id_book}', status_code=HTTPStatus.OK, response_model=Message)
async def delete_book(
    id_book: int,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    return await delete_book_with_id_service(session, id_book)
