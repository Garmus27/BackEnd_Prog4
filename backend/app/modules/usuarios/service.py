# app/modules/usuarios/service.py
from fastapi import HTTPException, status
from sqlmodel import Session

from app.core.config import settings
from app.core.security import hash_password, verify_password, create_access_token
from app.modules.usuarios.models import Usuario, UsuarioCreate, UsuarioPublic, Token
from app.modules.usuarios.unit_of_work import UsuarioUnitOfWork


class UsuarioService:
    def __init__(self, session: Session) -> None:
        self._session = session

    def register(self, data: UsuarioCreate) -> UsuarioPublic:
        with UsuarioUnitOfWork(self._session) as uow:
            if uow.usuarios.get_by_username(data.username):
                raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                    detail="El nombre de usuario ya está en uso")
            if uow.usuarios.get_by_email(data.email):
                raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                    detail="El email ya está registrado")
            usuario = Usuario(
                username=data.username,
                full_name=data.full_name,
                email=data.email,
                hashed_password=hash_password(data.password),
                role="user",
            )
            uow.usuarios.add(usuario)
            result = UsuarioPublic.model_validate(usuario)
        return result

    def authenticate(self, username: str, password: str) -> Token:
        with UsuarioUnitOfWork(self._session) as uow:
            user = uow.usuarios.get_by_username(username)
            if not user or not verify_password(password, user.hashed_password):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Credenciales incorrectas",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            if user.disabled:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail="Cuenta de usuario desactivada")
            access_token = create_access_token(
                data={"sub": user.username, "role": user.role}
            )
        return Token(
            access_token=access_token,
            token_type="bearer",
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        )

    def list_all(self) -> list[UsuarioPublic]:
        with UsuarioUnitOfWork(self._session) as uow:
            usuarios = uow.usuarios.get_all()
            result = [UsuarioPublic.model_validate(u) for u in usuarios]
        return result

    def set_disabled(self, user_id: int, disabled: bool) -> UsuarioPublic:
        with UsuarioUnitOfWork(self._session) as uow:
            user = uow.usuarios.get_by_id(user_id)
            if not user:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail="Usuario no encontrado")
            user.disabled = disabled
            uow.usuarios.add(user)
            result = UsuarioPublic.model_validate(user)
        return result
