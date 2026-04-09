from http import HTTPStatus

from fastapi import HTTPException

from app.core.security import create_access_token, verify_password
from app.repositories import user_repository


def authenticate_user(session, identifier: str, password: str):
    user = user_repository.get_user_by_identifier(session, identifier)

    if not user:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Incorrect email or password',
        )

    if not verify_password(password, user.password):
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Incorrect email or password',
        )

    access_token = create_access_token(data={'sub': user.email})

    return {'access_token': access_token, 'token_type': 'Bearer'}
