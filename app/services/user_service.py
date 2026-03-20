from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

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
                status_code=HTTPStatus.CONFLICT, detail='Email já existe'
            )

    user = User(
        username=user_schema.username,
        email=user_schema.email,
        password=user_schema.password,
    )

    user_repository.save(session, user)
    session.commit()
    session.refresh(user)

    return user


def update_user_service(session, user_schema, user_id: int):
    user = user_repository.get_by_id(session, user_id)

    if not user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Usuário não encontrado'
        )

    update_data = user_schema.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(user, field, value)

    try:
        session.add(user)
        session.commit()
        session.refresh(user)
        return user

    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT, detail='Nome ou Email já existe'
        )


def delete_user_service(session, user_id: int):
    user = user_repository.get_by_id(session, user_id)

    if not user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Usuário não encontrado'
        )

    session.delete(user)
    session.commit()

    return {'mensagem': 'Usuário deletado'}
