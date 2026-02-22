from http import HTTPStatus

from fastapi import HTTPException

from app.models import Conta
from app.repositories import conta_repository


def create_conta_service(session, conta_schema):
    db_conta = conta_repository.get_by_username_or_email(
        session, conta_schema.username, conta_schema.email
    )

    if db_conta:
        if db_conta.username == conta_schema.username:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='Nome de usuario já existe',
            )

        if db_conta.email == conta_schema.email:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT, detail='Email já existe'
            )

    user = Conta(
        username=conta_schema.username,
        email=conta_schema.email,
        password=conta_schema.password,
    )

    return conta_repository.create_conta(session, user)
