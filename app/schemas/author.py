from pydantic import BaseModel, ConfigDict, Field


class AuthorBase(BaseModel):
    name: str = Field(min_length=2, max_length=30)


class AuthorCreate(AuthorBase):
    pass


class AuthorUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=30)


class AuthorPublic(AuthorBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class FilterPage(BaseModel):
    offset: int = Field(ge=0, default=0)
    limit: int = Field(ge=0, default=10)


class Filter(FilterPage):
    name: str | None = Field(default=None, min_length=2, max_length=30)


class AuthorList(BaseModel):
    authors: list[AuthorPublic]


class Message(BaseModel):
    mensagem: str
