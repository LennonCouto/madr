from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from app.models.book import Book


def save(session: Session, book: Book):
    session.add(book)
    return book


async def get_by_title(session: AsyncSession, title: str):
    stmt = await session.scalar(select(Book).where(Book.title == title))
    return stmt


async def get_by_id_book(session: AsyncSession, id_book: int):
    stmt = await session.scalar(select(Book).where(Book.id == id_book))
    return stmt


def get_filter_book(
    session: Session,
    title: str | None,
    year: str | None,
    offset: int,
    limit: int,
):
    query = select(Book)

    if title:
        query = query.filter(Book.title.contains(title))

    if year:
        query = query.filter(Book.year.contains(year))

    books = session.scalars(query.offset(offset).limit(limit))

    return {'books': books.all()}
