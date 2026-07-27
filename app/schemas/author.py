from pydantic import BaseModel, ConfigDict


class AuthorBase(BaseModel):
    name: str


class AuthorCreate(AuthorBase):
    pass


class AuthorUpdate(BaseModel):
    name: str | None = None


class AuthorPublic(AuthorBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class Message(BaseModel):
    mensagem: str
