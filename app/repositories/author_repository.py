from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.author import Author


async def get_by_id_author(session: AsyncSession, author_id: int):
    stmt = await session.scalar(select(Author).where(Author.id == author_id))
    return stmt


async def get_by_name_author(session: AsyncSession, name: str):
    return await session.scalar(select(Author).where(Author.name == name))


async def get_author_with_filters(
    session: AsyncSession, name: str | None, offset: int, limit: int
):
    query = select(Author)

    if name:
        query = query.filter(Author.name.contains(name))

    authors = await session.scalars(query.offset(offset).limit(limit))

    return {'authors': authors.all()}


def save(session: AsyncSession, author: Author):
    session.add(author)
    return author
