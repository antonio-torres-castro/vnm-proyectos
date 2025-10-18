# backend/app/api/auth.py
from datetime import timedelta

from app.core.config import settings
from app.core.database import get_db
from app.core.security import (
    create_access_token,
    get_current_user,
    verify_password,
    verify_token,
)
from app.models.usuario import Usuario
from app.schemas.token import Token
from app.schemas.usuario import UsuarioLogin, UsuarioResponse
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    # Buscar usuario por email
    usuario = db.query(Usuario).filter(Usuario.email == form_data.username).first()

    if not usuario or not verify_password(form_data.password, str(usuario.clave_hash)):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Verificar si el usuario está activo
    if usuario.estado_id != 2:  # 1 = creado, 2 = activo
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no activo",
        )

    # Crear token de acceso
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        subject=usuario.email, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/login-form", response_model=Token)
async def login_form(usuario_data: UsuarioLogin, db: Session = Depends(get_db)):
    # Versión alternativa que recibe JSON en lugar de form-data
    usuario = db.query(Usuario).filter(Usuario.email == usuario_data.email).first()

    if not usuario or not verify_password(usuario_data.clave, str(usuario.clave_hash)):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
        )

    if usuario.estado_id != 2:  # 1 = creado, 2 = activo
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no activo",
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        subject=usuario.email, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/verify-token")
async def verify_token_endpoint(token: str):
    email = verify_token(token)
    if not email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado",
        )
    return {"email": email, "valid": True}


@router.get("/me", response_model=UsuarioResponse)
async def get_current_user_info(current_user: Usuario = Depends(get_current_user)):
    """Obtiene la información del usuario autenticado actualmente"""
    return current_user


@router.post("/logout")
async def logout(current_user: Usuario = Depends(get_current_user)):
    """Cerrar sesión del usuario actual"""
    # En aplicaciones JWT stateless, el logout se maneja principalmente en el cliente
    # eliminando el token. Este endpoint puede usarse para logs de auditoría.
    return {"message": "Sesión cerrada exitosamente", "success": True}
