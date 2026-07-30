from pydantic import BaseModel, ConfigDict, Field


class AuthorBase(BaseModel):
    name: str = Field(min_length=2, max_length=80)


class AuthorCreate(AuthorBase):
    pass


class AuthorUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=80)


class AuthorPublic(AuthorBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class Message(BaseModel):
    mensagem: str
