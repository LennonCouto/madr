from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from app.models.author import Author


async def get_by_id_author(session: AsyncSession, author_id: int):
    stmt = await session.scalar(select(Author).where(Author.id == author_id))
    return stmt


async def get_by_name_author(session: AsyncSession, name: str):
    return await session.scalar(select(Author).where(Author.name == name))


def get_author_with_filters(
    session: Session, name: str | None, offset: int, limit: int
):
    query = select(Author)

    if name:
        query = query.filter(Author.name.contains(name))

    authors = session.scalars(query.offset(offset).limit(limit))

    return {'authors': authors.all()}


def save(session: Session, author: Author):
    session.add(author)
    return author
