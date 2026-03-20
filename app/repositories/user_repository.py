from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import User


def save(session: Session, user: User):
    session.add(user)
    return user


def get_by_username_or_email(session: Session, username: str, email: str):
    stmt = session.scalar(
        select(User).where((User.username == username) | (User.email == email))
    )

    return stmt


def get_by_id(session: Session, user_id: int):
    stmt = session.scalar(select(User).where(User.id == user_id))
    return stmt


def filter_user(session: Session, limit: int, offset: int):
    users = session.scalars(select(User).limit(limit).offset(offset)).all()

    return users
