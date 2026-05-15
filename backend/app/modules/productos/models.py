# app/modules/productos/models.py
from typing import Optional, List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from app.modules.categorias.models import Categoria
    from app.modules.ingredientes.models import Ingrediente


class ProductoIngrediente(SQLModel, table=True):
    __tablename__ = "producto_ingrediente"

    producto_id: Optional[int] = Field(default=None, foreign_key="productos.id", primary_key=True)
    ingrediente_id: Optional[int] = Field(default=None, foreign_key="ingredientes.id", primary_key=True)
    cantidad: float = Field(gt=0)
    unidad: str = Field(min_length=1, max_length=50)

    producto: Optional["Producto"] = Relationship(back_populates="producto_ingredientes")
    ingrediente: Optional["Ingrediente"] = Relationship(back_populates="producto_ingredientes")


class Producto(SQLModel, table=True):
    __tablename__ = "productos"

    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(min_length=2, max_length=150, index=True)
    descripcion: Optional[str] = Field(default=None, max_length=500)
    precio: float = Field(gt=0)
    is_active: bool = Field(default=True)

    categoria_id: Optional[int] = Field(default=None, foreign_key="categorias.id")
    categoria: Optional["Categoria"] = Relationship(back_populates="productos")

    producto_ingredientes: List["ProductoIngrediente"] = Relationship(back_populates="producto")
