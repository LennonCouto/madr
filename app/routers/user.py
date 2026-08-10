from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.repositories.user_repository import filter_user
from app.schemas.user import (
    FilterPage,
    Message,
    UserList,
    UserPublic,
    UserSchema,
    UserUpdate,
)
from app.services.user_service import (
    create_user_service,
    delete_user_service,
    update_user_service,
)

router = APIRouter(prefix='/users', tags=['User'])


@router.post('/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
async def create_user(
    user: UserSchema, session: AsyncSession = Depends(get_session)
):
    return await create_user_service(session, user)


@router.get('/', status_code=HTTPStatus.OK, response_model=UserList)
async def read_users(
    filter_users: Annotated[FilterPage, Depends()],
    session: Annotated[AsyncSession, Depends(get_session)],
    current_user: User = Depends(get_current_user),
):
    users = await filter_user(session, filter_users.limit, filter_users.offset)

    return {'users': users}


@router.patch(
    '/{user_id}', status_code=HTTPStatus.OK, response_model=UserPublic
)
async def update_user(
    user_id: int,
    user: UserUpdate,
    session: Annotated[AsyncSession, Depends(get_session)],
    current_user: User = Depends(get_current_user),
):

    return await update_user_service(session, current_user, user, user_id)


@router.delete('/{user_id}', status_code=HTTPStatus.OK, response_model=Message)
async def delete_user(
    user_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    return await delete_user_service(session, current_user, user_id)
