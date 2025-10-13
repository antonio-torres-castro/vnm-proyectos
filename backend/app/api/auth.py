# backend/app/api/auth.py
from datetime import timedelta, datetime
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import verify_password, create_access_token, get_password_hash, verify_token
from app.core.config import settings
from app.schemas.token import Token
from app.schemas.usuario import UsuarioLogin, UsuarioResponse
from app.models.usuario import Usuario
from app.models import Estado, Rol

router = APIRouter()

@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    # Buscar usuario por email
    usuario = db.query(Usuario).filter(Usuario.email == form_data.username).first()

    if not usuario or not verify_password(form_data.password, usuario.clave_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Verificar si el usuario está activo
    if usuario.estado_id != 1:  # 1 = activo
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario inactivo",
        )

    # Crear token de acceso
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        subject=usuario.email, expires_delta=access_token_expires
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@router.post("/login-form", response_model=Token)
async def login_form(
    usuario_data: UsuarioLogin,
    db: Session = Depends(get_db)
):
    # Versión alternativa que recibe JSON en lugar de form-data
    usuario = db.query(Usuario).filter(Usuario.email == usuario_data.email).first()

    if not usuario or not verify_password(usuario_data.clave, usuario.clave_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
        )

    if usuario.estado_id != 1:  # 1 = activo
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario inactivo",
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        subject=usuario.email, expires_delta=access_token_expires
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@router.get("/verify-token")
async def verify_token_endpoint(token: str):
    email = verify_token(token)
    if not email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado",
        )
    return {"email": email, "valid": True}


@router.post("/fix-admin-password")
async def fix_admin_password(db: Session = Depends(get_db)):
    """Endpoint temporal para corregir el hash de contraseña del usuario administrador"""

    admin_email = "admin@monitoreo.cl"
    admin_user = db.query(Usuario).filter(Usuario.email == admin_email).first()

    if not admin_user:
        return {
            "error": "Usuario administrador no encontrado",
            "message": "Ejecuta primero los scripts SQL de inicialización de la base de datos",
            "sql_path": "database/init-data/02-datos-autenticacion.sql"
        }

    # Verificar hash actual
    current_hash = admin_user.clave_hash
    correct_password = "admin123"

    # Generar nuevo hash correcto
    new_hash = get_password_hash(correct_password)

    # Verificar si el hash actual funciona
    current_hash_works = verify_password(correct_password, current_hash)

    if current_hash_works:
        return {
            "message": "El hash de contraseña ya está correcto",
            "email": admin_email,
            "password_works": True,
            "current_hash": current_hash
        }

    # Actualizar con el hash correcto
    admin_user.clave_hash = new_hash
    admin_user.fecha_modificacion = datetime.utcnow()

    db.commit()

    # Verificar que funciona después de la corrección
    verification_result = verify_password(correct_password, new_hash)

    return {
        "message": "Hash de contraseña corregido exitosamente",
        "email": admin_email,
        "username": admin_user.nombre_usuario,
        "password": correct_password,
        "old_hash": current_hash,
        "new_hash": new_hash,
        "verification_successful": verification_result,
        "warning": "El hash placeholder del SQL ha sido reemplazado por un hash real"
    }

@router.post("/debug-password")
async def debug_password(email: str, password: str, db: Session = Depends(get_db)):
    """Endpoint temporal para debugging de contraseñas"""

    # Buscar usuario
    usuario = db.query(Usuario).filter(Usuario.email == email).first()
    if not usuario:
        return {"error": "Usuario no encontrado", "email": email}

    # Verificar contraseña
    password_valid = verify_password(password, usuario.clave_hash)

    # Generar nuevo hash para comparar
    new_hash = get_password_hash(password)

    return {
        "email": email,
        "usuario_encontrado": True,
        "nombre_usuario": usuario.nombre_usuario,
        "estado_id": usuario.estado_id,
        "rol_id": usuario.rol_id,
        "password_provided": password,
        "password_valid": password_valid,
        "stored_hash": usuario.clave_hash,
        "new_hash_for_comparison": new_hash,
        "hash_matches": usuario.clave_hash == new_hash
    }
