from pydantic import BaseModel, ConfigDict, Field


class BookBase(BaseModel):
    title: str = Field(min_length=2, max_length=80)
    year: str


class BookCreate(BookBase):
    author_id: int


class BookUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=2, max_length=80)
    year: str | None = None
    author_id: int | None = None


class BookPublic(BookBase):
    id: int
    author_id: int

    model_config = ConfigDict(from_attributes=True)


class Message(BaseModel):
    mensagem: str
