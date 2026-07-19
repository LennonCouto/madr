from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

from app.models.author import Author
from app.repositories.author_repository import (
    get_by_id_author,
    get_by_name_author,
    save,
)


def create_author_service(session, author_schema):
    author_db = get_by_name_author(session, author_schema.name)

    if author_db:
        if author_db.name == author_schema.name:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='Author já consta no MADR',
            )

    author = Author(name=author_schema.name)

    save(session, author)
    session.commit()
    session.refresh(author)

    return author


def get_id_author_service(session, name_author):
    author_in_the_db = get_by_id_author(session, name_author)

    if not author_in_the_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Author não consta no MADR',
        )

    return author_in_the_db


def get_name_author_service(session, name_author):
    author_in_the_db = get_by_name_author(session, name_author)

    if not author_in_the_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Author não consta no MADR',
        )

    return author_in_the_db


def update_name_author(session, author_schema, id_author):
    author_in_the_db = get_by_id_author(session, id_author)

    if not author_in_the_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Author não consta no MADR',
        )

    for key, value in author_schema.model_dump(exclude_unset=True).items():
        setattr(author_in_the_db, key, value)

    try:
        session.add(author_in_the_db)
        session.commit()
        session.refresh(author_in_the_db)
        return author_in_the_db

    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT, detail='Author já consta no MADR'
        )


def delete_author_with_id(session, id_author):
    author_in_the_db = get_by_id_author(session, id_author)

    if not author_in_the_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='ID não consta no MADR',
        )

    session.delete(author_in_the_db)
    session.commit()

    return {'mensagem': 'Author deletado do MARD'}
