from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

from app.core.sanitizers import sanitize_name
from app.models.author import Author
from app.repositories.author_repository import (
    get_by_id_author,
    get_by_name_author,
    save,
)


async def create_author_service(session, author_schema):
    author_db = await get_by_name_author(session, author_schema.name)

    if author_db:
        if author_db.name == author_schema.name:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='Author já consta no MADR',
            )

    author = Author(name=sanitize_name(author_schema.name))

    save(session, author)
    await session.commit()
    await session.refresh(author)

    return author


async def get_id_author_service(session, name_author):
    author_in_the_db = await get_by_id_author(session, name_author)

    if not author_in_the_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Author não consta no MADR',
        )

    return author_in_the_db


async def update_name_author(session, author_schema, id_author):
    author_in_the_db = await get_by_id_author(session, id_author)

    if not author_in_the_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Author não consta no MADR',
        )

    for key, value in author_schema.model_dump(exclude_unset=True).items():
        processed_value = value
        if key == 'name':
            processed_value = sanitize_name(processed_value)
        setattr(author_in_the_db, key, processed_value)

    try:
        session.add(author_in_the_db)
        await session.commit()
        await session.refresh(author_in_the_db)
        return author_in_the_db

    except IntegrityError:
        await session.rollback()
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT, detail='Author já consta no MADR'
        )


async def delete_author_with_id(session, id_author):
    author_in_the_db = await get_by_id_author(session, id_author)

    if not author_in_the_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Author não consta no MADR',
        )

    await session.delete(author_in_the_db)
    await session.commit()

    return {'mensagem': 'Author deletado do MADR'}
