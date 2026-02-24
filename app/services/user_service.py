from http import HTTPStatus

from fastapi import HTTPException

from app.models import User
from app.repositories import user_repository


def create_user_service(session, user_schema):
    db_user = user_repository.get_by_username_or_email(
        session, user_schema.username, user_schema.email
    )

    if db_user:
        if db_user.username == user_schema.username:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='Nome de usuario já existe',
            )

        if db_user.email == user_schema.email:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='Email já existe'
            )

    user = User(
        username=user_schema.username,
        email=user_schema.email,
        password=user_schema.password,
    )

    return user_repository.create_user(session, user)
