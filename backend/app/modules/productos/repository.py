# app/modules/productos/repository.py
from sqlmodel import Session, select
from sqlalchemy.orm import selectinload
from app.core.repository import BaseRepository
from app.modules.productos.models import Producto, ProductoIngrediente


class ProductoRepository(BaseRepository[Producto]):
    def __init__(self, session: Session) -> None:
        super().__init__(session, Producto)

    def get_active(self, offset: int = 0, limit: int = 20) -> list[Producto]:
        return list(self.session.exec(
            select(Producto).where(Producto.is_active == True).offset(offset).limit(limit)
        ).all())

    def get_by_id_con_detalle(self, producto_id: int) -> Producto | None:
        statement = (
            select(Producto)
            .where(Producto.id == producto_id)
            .options(
                selectinload(Producto.categoria),
                selectinload(Producto.producto_ingredientes).selectinload(
                    ProductoIngrediente.ingrediente
                ),
            )
        )
        return self.session.exec(statement).first()

    def count(self) -> int:
        return len(self.session.exec(select(Producto)).all())


class ProductoIngredienteRepository(BaseRepository[ProductoIngrediente]):
    def __init__(self, session: Session) -> None:
        super().__init__(session, ProductoIngrediente)

    def get_by_ids(self, producto_id: int, ingrediente_id: int) -> ProductoIngrediente | None:
        return self.session.exec(
            select(ProductoIngrediente)
            .where(ProductoIngrediente.producto_id == producto_id)
            .where(ProductoIngrediente.ingrediente_id == ingrediente_id)
        ).first()
