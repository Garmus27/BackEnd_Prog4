# app/modules/usuarios/models.py
from typing import Optional
from sqlmodel import SQLModel, Field
from pydantic import EmailStr


class Usuario(SQLModel, table=True):
    __tablename__ = "usuarios"

    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(unique=True, index=True)
    full_name: str
    email: str = Field(unique=True, index=True)
    hashed_password: str
    role: str = Field(default="user")   # "user" | "admin"
    disabled: bool = Field(default=False)


class UsuarioCreate(SQLModel):
    username: str
    full_name: str
    email: EmailStr
    password: str = Field(min_length=8)


class UsuarioPublic(SQLModel):
    id: int
    username: str
    full_name: str
    email: str
    role: str
    disabled: bool


class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
