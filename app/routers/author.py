from http import HTTPStatus

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_session
from app.schemas.author import AuthorPublic, AuthorSchema
from app.services.author_service import create_author_service

router = APIRouter(prefix='/author', tags=['Author'])


@router.post('/', status_code=HTTPStatus.CREATED, response_model=AuthorPublic)
def create_author(
    author: AuthorSchema, session: Session = Depends(get_session)
):
    return create_author_service(session, author)
