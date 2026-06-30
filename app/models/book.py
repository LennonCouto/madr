from sqlalchemy.orm import Mapped, mapped_column

from app.db.registry import table_registry


@table_registry.mapped_as_dataclass
class Book:
    __tablename__ = 'books'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    year: Mapped[str]
    title: Mapped[str] = mapped_column(unique=True)
