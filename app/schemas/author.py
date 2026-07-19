from pydantic import BaseModel


class AuthorSchema(BaseModel):
    name: str


class AuthorPublic(AuthorSchema):
    id: int


class AuthorUpdate(BaseModel):
    name: str | None = None
