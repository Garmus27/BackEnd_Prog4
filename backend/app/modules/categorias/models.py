# app/modules/categorias/models.py
from typing import Optional, List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from app.modules.productos.models import Producto


class Categoria(SQLModel, table=True):
    __tablename__ = "categorias"

    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(min_length=2, max_length=100, unique=True, index=True)
    descripcion: Optional[str] = Field(default=None, max_length=300)
    is_active: bool = Field(default=True)

    productos: List["Producto"] = Relationship(back_populates="categoria")
