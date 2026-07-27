from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.registry import table_registry

if TYPE_CHECKING:
    from app.models.author import Author


@table_registry.mapped_as_dataclass
class Book:
    __tablename__ = 'books'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    year: Mapped[str]
    title: Mapped[str] = mapped_column(unique=True)

    author_id: Mapped[int] = mapped_column(ForeignKey('authors.id'))
    author: Mapped['Author'] = relationship(back_populates='books', init=False)
