from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.db.session import get_session
from app.schemas.token import Token
from app.services.auth_service import authenticate_user

router = APIRouter()


@router.post('/login', response_model=Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session),
):
    return authenticate_user(session, form_data.username, form_data.password)
