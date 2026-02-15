from http import HTTPStatus

from fastapi import APIRouter

from madr.schemas.user import UserPublic, UserSchema

router = APIRouter(prefix='/conta', tags=['conta'])


@router.post('/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_conta(user: UserSchema):
    user_data = user.model_dump()
    user_data['id'] = 1

    return user_data
