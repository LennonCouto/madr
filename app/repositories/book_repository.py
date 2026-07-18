from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.book import Book


def save(session: Session, book: Book):
    session.add(book)
    return book


def get_by_title(session: Session, title: str):
    stmt = session.scalar(select(Book).where(Book.title == title))
    return stmt


def get_by_id_book(session: Session, id_book: int):
    stmt = session.scalar(select(Book).where(Book.id == id_book))
    return stmt
