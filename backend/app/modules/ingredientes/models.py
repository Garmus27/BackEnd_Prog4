# app/modules/ingredientes/models.py
from typing import Optional, List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from app.modules.productos.models import ProductoIngrediente


class Ingrediente(SQLModel, table=True):
    __tablename__ = "ingredientes"

    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(min_length=2, max_length=100, unique=True, index=True)
    unidad_medida: str = Field(min_length=1, max_length=50)
    is_active: bool = Field(default=True)

    producto_ingredientes: List["ProductoIngrediente"] = Relationship(back_populates="ingrediente")
