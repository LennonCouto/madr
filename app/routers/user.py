from http import HTTPStatus

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_session
from app.schemas.user import UserPublic, UserSchema, UserUpdate, UserList, FilterPage
from app.services.user_service import create_user_service, update_user_service
from app.repositories.user_repository import filter_user

router = APIRouter(prefix='/conta', tags=['User'])


@router.post('/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema, session: Session = Depends(get_session)):
    return create_user_service(session, user)


@router.get('/', status_code=HTTPStatus.OK, response_model=UserList)
def read_users(filter_users: FilterPage = Depends(), session: Session = Depends(get_session)):
    users = filter_user(session, filter_users.limit, filter_users.offset)

    return {'users': users}


@router.patch(
    '/{user_id}', status_code=HTTPStatus.OK, response_model=UserPublic
)
def update_user(
    user_id: int, user: UserUpdate, session: Session = Depends(get_session)
):
    return update_user_service(session, user, user_id)


