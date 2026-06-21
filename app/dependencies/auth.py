from http import HTTPStatus

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import DecodeError, decode
from sqlalchemy.orm import Session

from app.core.security import settings
from app.db.session import get_session
from app.repositories.user_repository import get_user_by_identifier

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')


def get_current_user(
    session: Session = Depends(get_session),
    token: str = Depends(oauth2_scheme),
):

    credentials_exception = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail='Você não possui credenciais válidas',
        headers={'WWW-Authenticate': 'Bearer'},
    )

    try:
        payload = decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )
        subject = payload.get('sub')
        if not subject:
            raise credentials_exception
    except DecodeError:
        raise credentials_exception

    user = get_user_by_identifier(session, subject)

    if not user:
        raise credentials_exception

    return user
