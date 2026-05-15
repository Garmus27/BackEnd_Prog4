# app/modules/ingredientes/schemas.py
from typing import Optional, List
from sqlmodel import SQLModel, Field


class IngredienteCreate(SQLModel):
    nombre: str = Field(min_length=2, max_length=100)
    unidad_medida: str = Field(min_length=1, max_length=50)


class IngredienteUpdate(SQLModel):
    nombre: Optional[str] = Field(default=None, min_length=2, max_length=100)
    unidad_medida: Optional[str] = Field(default=None, min_length=1, max_length=50)
    is_active: Optional[bool] = None


class IngredientePublic(SQLModel):
    id: int
    nombre: str
    unidad_medida: str
    is_active: bool


class IngredienteList(SQLModel):
    data: List[IngredientePublic]
    total: int
