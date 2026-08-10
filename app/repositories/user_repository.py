from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from app.models import User


def save(session: Session, user: User):
    session.add(user)
    return user


async def get_by_username_or_email(
    session: AsyncSession, username: str, email: str
):
    stmt = await session.scalar(
        select(User).where((User.username == username) | (User.email == email))
    )

    return stmt


async def get_by_id(session: AsyncSession, user_id: int):
    stmt = await session.scalar(select(User).where(User.id == user_id))
    return stmt


async def filter_user(session: AsyncSession, limit: int, offset: int):
    users = await session.scalars(
        select(User).limit(limit).offset(offset))

    return users.all()


async def get_user_by_identifier(session: AsyncSession, identifier: str):
    stmt = select(User).where(
        (User.username == identifier) | (User.email == identifier)
    )
    return await session.scalar(stmt)
