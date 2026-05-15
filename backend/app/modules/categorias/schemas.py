# app/modules/categorias/schemas.py
from typing import Optional, List
from sqlmodel import SQLModel, Field


class CategoriaCreate(SQLModel):
    nombre: str = Field(min_length=2, max_length=100)
    descripcion: Optional[str] = Field(default=None, max_length=300)


class CategoriaUpdate(SQLModel):
    nombre: Optional[str] = Field(default=None, min_length=2, max_length=100)
    descripcion: Optional[str] = Field(default=None, max_length=300)
    is_active: Optional[bool] = None


class CategoriaPublic(SQLModel):
    id: int
    nombre: str
    descripcion: Optional[str] = None
    is_active: bool


class CategoriaList(SQLModel):
    data: List[CategoriaPublic]
    total: int
