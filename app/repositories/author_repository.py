from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.author import Author


def get_by_id_author(session: Session, id_author: int):
    stmt = session.scalar(select(Author).where(Author.id == id_author))
    return stmt


def get_by_author(session: Session, name_author: str):
    stmt = session.scalar(select(Author).where(Author.name == name_author))
    return stmt


def save(session: Session, author: Author):
    session.add(author)
    return author
