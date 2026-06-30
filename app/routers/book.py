from http import HTTPStatus

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_session
from app.schemas.book import BookPublic, BookSchema
from app.services.book_service import create_book_service

router = APIRouter(prefix='/book', tags=['Book'])


@router.post('/', status_code=HTTPStatus.CREATED, response_model=BookPublic)
def create_book(book: BookSchema, session: Session = Depends(get_session)):
    return create_book_service(session, book)
