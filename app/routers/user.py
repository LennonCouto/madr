from http import HTTPStatus

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_session
from app.schemas.user import UserPublic, UserSchema, UserUpdate
from app.services.user_service import create_user_service, update_user_service

router = APIRouter(prefix='/conta', tags=['User'])


@router.post('/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema, session: Session = Depends(get_session)):
    return create_user_service(session, user)


@router.patch(
    '/{user_id}', status_code=HTTPStatus.OK, response_model=UserPublic
)
def update_user(
    user_id: int, user: UserUpdate, session: Session = Depends(get_session)
):
    return update_user_service(session, user, user_id)
