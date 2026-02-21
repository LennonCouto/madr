from http import HTTPStatus

from fastapi import Depends, APIRouter

from app.schemas.conta import UserPublic, UserSchema
from app.db.session import get_session
from app.models.conta import Conta

router = APIRouter(prefix='/conta', tags=['conta'])


@router.post('/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_conta(user: UserSchema, session: Session = Depends(get_session)):
    db_user = Conta(
        username=user.username, password=user.password, email=user.email
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user