from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    username: str
    email: EmailStr


class HobbyCreate(BaseModel):
    name: str
    category: str | None = None
    fields: dict = {}  # campos livres definidos pelo usuário


class HobbyUpdate(BaseModel):
    name: str | None = None
    category: str | None = None
    fields: dict | None = None
