from pydantic import BaseModel, ConfigDict


class BookBase(BaseModel):
    title: str
    year: str


class BookCreate(BookBase):
    author_id: int


class BookUpdate(BaseModel):
    title: str | None = None
    year: str | None = None
    author_id: int | None = None


class BookPublic(BookBase):
    id: int
    author_id: int

    model_config = ConfigDict(from_attributes=True)


class Message(BaseModel):
    mensagem: str
