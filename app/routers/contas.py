from http import HTTPStatus

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_session
from app.schemas.conta import UserPublic, UserSchema
from app.services.conta_service import create_conta_service

router = APIRouter(prefix='/conta', tags=['conta'])


@router.post('/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_conta(conta: UserSchema, session: Session = Depends(get_session)):
    return create_conta_service(session, conta)
