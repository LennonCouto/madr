from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import User


def get_by_username_or_email(session: Session, username: str, email: str):
    stmt = session.scalar(
        select(User).where((User.username == username) | (User.email == email))
    )

    return stmt


def create_user(session: Session, user: User):
    session.add(user)
    session.commit()
    session.refresh(user)

    return user
