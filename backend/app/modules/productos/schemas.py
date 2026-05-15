# app/modules/productos/schemas.py
from typing import Optional, List
from sqlmodel import SQLModel, Field

from app.modules.categorias.schemas import CategoriaPublic
from app.modules.ingredientes.schemas import IngredientePublic


class ProductoIngredienteCreate(SQLModel):
    ingrediente_id: int
    cantidad: float = Field(gt=0)
    unidad: str = Field(min_length=1, max_length=50)


class ProductoIngredientePublic(SQLModel):
    ingrediente_id: int
    cantidad: float
    unidad: str
    ingrediente: Optional[IngredientePublic] = None


class ProductoCreate(SQLModel):
    nombre: str = Field(min_length=2, max_length=150)
    descripcion: Optional[str] = Field(default=None, max_length=500)
    precio: float = Field(gt=0)
    categoria_id: Optional[int] = None


class ProductoUpdate(SQLModel):
    nombre: Optional[str] = Field(default=None, min_length=2, max_length=150)
    descripcion: Optional[str] = Field(default=None, max_length=500)
    precio: Optional[float] = Field(default=None, gt=0)
    categoria_id: Optional[int] = None
    is_active: Optional[bool] = None


class ProductoPublic(SQLModel):
    id: int
    nombre: str
    descripcion: Optional[str] = None
    precio: float
    is_active: bool
    categoria_id: Optional[int] = None


class ProductoList(SQLModel):
    data: List[ProductoPublic]
    total: int


class ProductoConDetalle(SQLModel):
    id: int
    nombre: str
    descripcion: Optional[str] = None
    precio: float
    is_active: bool
    categoria_id: Optional[int] = None
    categoria: Optional[CategoriaPublic] = None
    ingredientes: List[ProductoIngredientePublic] = []

    model_config = {"from_attributes": True}
