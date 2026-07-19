from http import HTTPStatus

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_session
from app.schemas.author import (
    AuthorPublic,
    AuthorSchema,
    AuthorUpdate,
    Message,
)
from app.services.author_service import (
    create_author_service,
    delete_author_with_id,
    get_id_author_service,
    get_name_author_service,
    update_name_author,
)

router = APIRouter(prefix='/author', tags=['Author'])


@router.post('/', status_code=HTTPStatus.CREATED, response_model=AuthorPublic)
def create_author(
    author: AuthorSchema, session: Session = Depends(get_session)
):
    return create_author_service(session, author)


@router.get(
    '/{id_author}', status_code=HTTPStatus.OK, response_model=AuthorPublic
)
def get_id_author(id_author: int, session: Session = Depends(get_session)):
    return get_id_author_service(session, id_author)


@router.get('/', status_code=HTTPStatus.OK, response_model=AuthorPublic)
def get_name_author(author_name: str, session: Session = Depends(get_session)):
    return get_name_author_service(session, author_name)


@router.patch('/', status_code=HTTPStatus.OK, response_model=AuthorPublic)
def update_author(
    id_author: int,
    author: AuthorUpdate,
    session: Session = Depends(get_session),
):
    return update_name_author(session, author, id_author)


@router.delete('/', status_code=HTTPStatus.OK, response_model=Message)
def delete_author(id_author: int, session: Session = Depends(get_session)):
    return delete_author_with_id(session, id_author)
