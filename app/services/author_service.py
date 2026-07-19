from http import HTTPStatus

from fastapi import HTTPException

from app.models.author import Author
from app.repositories.author_repository import get_by_author, save


def create_author_service(session, author_schema):
    author_db = get_by_author(session, author_schema.name)

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
