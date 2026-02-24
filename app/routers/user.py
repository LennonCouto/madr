from http import HTTPStatus

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_session
from app.schemas.user import UserPublic, UserSchema
from app.services.user_service import create_user_service

router = APIRouter(prefix='/users', tags=['User'])


@router.post('/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema, session: Session = Depends(get_session)):
    return create_user_service(session, user)
