from __future__ import annotations

from typing import TYPE_CHECKING, List

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.registry import table_registry

if TYPE_CHECKING:
    from app.models.book import Book


@table_registry.mapped_as_dataclass
class Author:
    __tablename__ = 'authors'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)

    books: Mapped[List['Book']] = relationship(
        back_populates='author', init=False
    )
