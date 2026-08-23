from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.token import Token
from app.services.auth_service import authenticate_user, new_token

router = APIRouter(prefix='/auth', tags=['auth'])


@router.post('/login', response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: Annotated[AsyncSession, Depends(get_session)],
):
    return await authenticate_user(
        session, form_data.username, form_data.password
    )


@router.post('/refresh_token', response_model=Token)
async def reflesh_access_token(
    user: Annotated[User, Depends(get_current_user)],
):
    return await new_token(user)
