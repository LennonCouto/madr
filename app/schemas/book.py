from pydantic import BaseModel


class BookSchema(BaseModel):
    title: str
    year: str


class BookPublic(BookSchema):
    id: int


class BookUpdate(BaseModel):
    title: str | None = None
    year: str | None = None
