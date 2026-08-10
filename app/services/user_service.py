from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

from app.core import security
from app.core.sanitizers import sanitize_name
from app.models import User
from app.repositories import user_repository


async def create_user_service(session, user_schema):
    db_user = await user_repository.get_by_username_or_email(
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

    hashed_password = security.get_password_hash(user_schema.password)

    user = User(
        username=sanitize_name(user_schema.username),
        email=user_schema.email,
        password=hashed_password,
    )

    user_repository.save(session, user)
    await session.commit()
    await session.refresh(user)

    return user


async def update_user_service(
    session, current_user, user_schema, user_id: int
):
    user = await user_repository.get_by_id(session, user_id)

    if not user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Usuário não encontrado'
        )

    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail='Sem permição suficiente'
        )

    update_data = user_schema.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        processed_value = value
        if key == 'password':
            processed_value = security.get_password_hash(value)
        if key == 'username':
            processed_value = sanitize_name(value)
        setattr(user, key, processed_value)

    try:
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user

    except IntegrityError:
        await session.rollback()
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT, detail='Nome ou Email já existe'
        )


async def delete_user_service(session, current_user, user_id: int):
    user = await user_repository.get_by_id(session, user_id)

    if not user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Usuário não encontrado'
        )

    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail='Sem permição suficiente'
        )

    await session.delete(user)
    await session.commit()

    return {'mensagem': 'Usuário deletado'}
