# app/modules/usuarios/router.py
from typing import Annotated
from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session

from app.core.database import get_session
from app.core.deps import get_current_active_user, require_role
from app.modules.usuarios.models import UsuarioCreate, UsuarioPublic, Token
from app.modules.usuarios.service import UsuarioService

router = APIRouter()


def get_service(session: Annotated[Session, Depends(get_session)]) -> UsuarioService:
    return UsuarioService(session)


# ── Registro ──────────────────────────────────────────────────────────────────

@router.post("/register", response_model=UsuarioPublic, status_code=status.HTTP_201_CREATED)
def register(
    data: UsuarioCreate,
    svc: Annotated[UsuarioService, Depends(get_service)],
):
    return svc.register(data)


# ── Login ─────────────────────────────────────────────────────────────────────

@router.post("/token", response_model=Token)
def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    svc: Annotated[UsuarioService, Depends(get_service)],
):
    return svc.authenticate(form_data.username, form_data.password)


# ── Usuario autenticado ───────────────────────────────────────────────────────

@router.get("/me", response_model=UsuarioPublic)
def read_me(
    current_user: Annotated[UsuarioPublic, Depends(get_current_active_user)],
):
    return current_user


# ── Administración (solo admin) ───────────────────────────────────────────────

@router.get("/admin/usuarios", response_model=list[UsuarioPublic])
def list_users(
    _admin: Annotated[UsuarioPublic, Depends(require_role(["admin"]))],
    svc: Annotated[UsuarioService, Depends(get_service)],
):
    return svc.list_all()


@router.post("/admin/usuarios/{user_id}/desactivar", response_model=UsuarioPublic)
def deactivate_user(
    user_id: int,
    _admin: Annotated[UsuarioPublic, Depends(require_role(["admin"]))],
    svc: Annotated[UsuarioService, Depends(get_service)],
):
    return svc.set_disabled(user_id, disabled=True)


@router.post("/admin/usuarios/{user_id}/activar", response_model=UsuarioPublic)
def activate_user(
    user_id: int,
    _admin: Annotated[UsuarioPublic, Depends(require_role(["admin"]))],
    svc: Annotated[UsuarioService, Depends(get_service)],
):
    return svc.set_disabled(user_id, disabled=False)
