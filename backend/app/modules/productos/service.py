# app/modules/productos/service.py
from fastapi import HTTPException, status
from sqlmodel import Session

from app.modules.productos.models import Producto, ProductoIngrediente
from app.modules.productos.schemas import (
    ProductoCreate, ProductoPublic, ProductoUpdate, ProductoList,
    ProductoConDetalle, ProductoIngredienteCreate, ProductoIngredientePublic,
)
from app.modules.ingredientes.schemas import IngredientePublic
from app.modules.productos.unit_of_work import ProductoUnitOfWork


class ProductoService:
    def __init__(self, session: Session) -> None:
        self._session = session

    def _get_or_404(self, uow, producto_id: int) -> Producto:
        producto = uow.productos.get_by_id(producto_id)
        if not producto:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Producto con id={producto_id} no encontrado")
        return producto

    def _get_categoria_or_404(self, uow, categoria_id: int):
        categoria = uow.categorias.get_by_id(categoria_id)
        if not categoria:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Categoria con id={categoria_id} no encontrada")
        return categoria

    def _get_ingrediente_or_404(self, uow, ingrediente_id: int):
        ingrediente = uow.ingredientes.get_by_id(ingrediente_id)
        if not ingrediente:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Ingrediente con id={ingrediente_id} no encontrado")
        return ingrediente

    def _build_detalle(self, uow, producto_id: int) -> ProductoConDetalle:
        producto = uow.productos.get_by_id_con_detalle(producto_id)
        if not producto:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Producto con id={producto_id} no encontrado")
        ingredientes_data = []
        for pi in producto.producto_ingredientes:
            ing = IngredientePublic.model_validate(pi.ingrediente) if pi.ingrediente else None
            ingredientes_data.append(ProductoIngredientePublic(
                ingrediente_id=pi.ingrediente_id,
                cantidad=pi.cantidad,
                unidad=pi.unidad,
                ingrediente=ing,
            ))
        from app.modules.categorias.schemas import CategoriaPublic
        return ProductoConDetalle(
            id=producto.id,
            nombre=producto.nombre,
            descripcion=producto.descripcion,
            precio=producto.precio,
            is_active=producto.is_active,
            categoria_id=producto.categoria_id,
            categoria=CategoriaPublic.model_validate(producto.categoria) if producto.categoria else None,
            ingredientes=ingredientes_data,
        )

    def create(self, data: ProductoCreate) -> ProductoPublic:
        with ProductoUnitOfWork(self._session) as uow:
            if data.categoria_id:
                self._get_categoria_or_404(uow, data.categoria_id)
            producto = Producto.model_validate(data)
            uow.productos.add(producto)
            result = ProductoPublic.model_validate(producto)
        return result

    def get_all(self, offset: int = 0, limit: int = 20) -> ProductoList:
        with ProductoUnitOfWork(self._session) as uow:
            productos = uow.productos.get_active(offset=offset, limit=limit)
            total = uow.productos.count()
            result = ProductoList(
                data=[ProductoPublic.model_validate(p) for p in productos],
                total=total,
            )
        return result

    def get_by_id(self, producto_id: int) -> ProductoConDetalle:
        with ProductoUnitOfWork(self._session) as uow:
            result = self._build_detalle(uow, producto_id)
        return result

    def update(self, producto_id: int, data: ProductoUpdate) -> ProductoPublic:
        with ProductoUnitOfWork(self._session) as uow:
            producto = self._get_or_404(uow, producto_id)
            if data.categoria_id and data.categoria_id != producto.categoria_id:
                self._get_categoria_or_404(uow, data.categoria_id)
            for field, value in data.model_dump(exclude_unset=True).items():
                setattr(producto, field, value)
            uow.productos.add(producto)
            result = ProductoPublic.model_validate(producto)
        return result

    def delete(self, producto_id: int) -> None:
        with ProductoUnitOfWork(self._session) as uow:
            producto = self._get_or_404(uow, producto_id)
            producto.is_active = False
            uow.productos.add(producto)

    def agregar_ingrediente(self, producto_id: int, data: ProductoIngredienteCreate) -> ProductoConDetalle:
        with ProductoUnitOfWork(self._session) as uow:
            self._get_or_404(uow, producto_id)
            self._get_ingrediente_or_404(uow, data.ingrediente_id)
            if uow.producto_ingredientes.get_by_ids(producto_id, data.ingrediente_id):
                raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                    detail=f"El ingrediente id={data.ingrediente_id} ya está asociado al producto id={producto_id}")
            pi = ProductoIngrediente(
                producto_id=producto_id,
                ingrediente_id=data.ingrediente_id,
                cantidad=data.cantidad,
                unidad=data.unidad,
            )
            uow.producto_ingredientes.add(pi)
            result = self._build_detalle(uow, producto_id)
        return result

    def quitar_ingrediente(self, producto_id: int, ingrediente_id: int) -> ProductoConDetalle:
        with ProductoUnitOfWork(self._session) as uow:
            self._get_or_404(uow, producto_id)
            pi = uow.producto_ingredientes.get_by_ids(producto_id, ingrediente_id)
            if not pi:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail=f"El ingrediente id={ingrediente_id} no está asociado al producto id={producto_id}")
            uow.producto_ingredientes.delete(pi)
            result = self._build_detalle(uow, producto_id)
        return result
