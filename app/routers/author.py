from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.repositories.author_repository import get_author_with_filters
from app.schemas.author import (
    AuthorCreate,
    AuthorList,
    AuthorPublic,
    AuthorUpdate,
    Filter,
    Message,
)
from app.services.author_service import (
    create_author_service,
    delete_author_with_id,
    get_id_author_service,
    update_name_author,
)

router = APIRouter(prefix='/author', tags=['Author'])


@router.post('/', status_code=HTTPStatus.CREATED, response_model=AuthorPublic)
async def create_author(
    author: AuthorCreate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    return await create_author_service(session, author)


@router.get(
    '/{id_author}', status_code=HTTPStatus.OK, response_model=AuthorPublic
)
async def get_id_author(
    id_author: int,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    return await get_id_author_service(session, id_author)


@router.get('/', response_model=AuthorList)
def get_authors(
    filter: Annotated[Filter, Query()],
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    return get_author_with_filters(
        session, filter.name, filter.offset, filter.limit
    )


@router.patch(
    '/{id_author}', status_code=HTTPStatus.OK, response_model=AuthorPublic
)
async def update_author(
    id_author: int,
    author: AuthorUpdate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    return await update_name_author(session, author, id_author)


@router.delete(
    '/{id_author}', status_code=HTTPStatus.OK, response_model=Message
)
async def delete_author(
    id_author: int,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    return await delete_author_with_id(session, id_author)
