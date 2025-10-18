# backend/app/api/usuarios.py
from typing import List, Optional

from app.core.database import get_db
from app.core.security import get_current_user
from app.models import Usuario
from app.schemas.usuario import (
    UsuarioChangePassword,
    UsuarioCreate,
    UsuarioDetallado,
    UsuarioListResponse,
    UsuarioResponse,
    UsuarioUpdate,
)
from app.schemas.usuario_historia import UsuarioHistoriaResponse
from app.services.usuario_service import UsuarioService
from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from sqlalchemy.orm import Session

router = APIRouter()


@router.post(
    "/crear-admin",
    response_model=UsuarioResponse,
    status_code=status.HTTP_201_CREATED,
)
async def crear_usuario_administrador(
    request: Request,
    db: Session = Depends(get_db),
):
    """
    Crear usuario administrador inicial - Solo funciona si no existe ningún admin
    Endpoint público para bootstrap del sistema
    """

    # Verificar si ya existe un usuario administrador
    admin_existente = db.query(Usuario).filter(Usuario.rol_id == 1).first()
    if admin_existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ya existe un usuario administrador: {admin_existente.email}",
        )

    # Verificar si ya existe el email específico
    email_existente = (
        db.query(Usuario).filter(Usuario.email == "admin@monitoreo.cl").first()
    )
    if email_existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El email admin@monitoreo.cl ya existe en el sistema",
        )

    # Datos del administrador inicial
    admin_data = UsuarioCreate(
        email="admin@monitoreo.cl",
        nombre_usuario="Administrador",
        clave="admin123",
        rol_id=1,  # Administrador
        estado_id=2,  # Activo
    )

    try:
        ip_address, user_agent = get_client_info(request)

        # Crear usuario administrador usando el servicio
        usuario = UsuarioService.create(
            db=db,
            usuario_data=admin_data,
            usuario_creador_id=None,  # Bootstrap - no hay usuario creador
            ip_address=ip_address,
            user_agent=user_agent,
        )

        return usuario

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error de validación: {str(e)}",
        )
    except Exception as e:
        # Capturar errores de base de datos como duplicate key
        error_msg = str(e)
        if "duplicate key" in error_msg or "already exists" in error_msg:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Error de secuencia PostgreSQL. Ejecuta: python reparar_secuencia_usuario.py",
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error creando usuario administrador: {error_msg}",
            )


def get_client_info(request: Request) -> tuple[str, str]:
    """Extraer información del cliente para auditoría"""
    ip_address = request.client.host
    user_agent = request.headers.get("user-agent", "")
    return ip_address, user_agent


@router.get("/", response_model=UsuarioListResponse)
async def get_usuarios(
    skip: int = Query(0, ge=0, description="Registros a omitir"),
    limit: int = Query(50, ge=1, le=100, description="Máximo registros por página"),
    search: Optional[str] = Query(None, description="Buscar por email o nombre"),
    rol_id: Optional[int] = Query(None, description="Filtrar por rol"),
    estado_id: Optional[int] = Query(None, description="Filtrar por estado"),
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    """Obtener lista de usuarios con filtros y paginación"""

    usuarios, total = UsuarioService.get_all(
        db=db, skip=skip, limit=limit, search=search, rol_id=rol_id, estado_id=estado_id
    )

    total_paginas = (total + limit - 1) // limit

    return UsuarioListResponse(
        usuarios=usuarios,
        total=total,
        pagina=(skip // limit) + 1,
        por_pagina=limit,
        total_paginas=total_paginas,
    )


@router.get("/{usuario_id}", response_model=UsuarioDetallado)
async def get_usuario(
    usuario_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    """Obtener usuario por ID"""

    usuario = UsuarioService.get_by_id(db, usuario_id)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado"
        )

    # Convertir a UsuarioDetallado con información relacionada
    usuario_detallado = UsuarioDetallado(
        **usuario.__dict__,
        rol_nombre=usuario.rol.nombre if usuario.rol else None,
        estado_nombre=usuario.estado.nombre if usuario.estado else None,
    )

    return usuario_detallado


@router.post("/", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
async def create_usuario(
    usuario_data: UsuarioCreate,
    request: Request,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    """Crear nuevo usuario"""

    try:
        ip_address, user_agent = get_client_info(request)

        usuario = UsuarioService.create(
            db=db,
            usuario_data=usuario_data,
            usuario_creador_id=current_user.id,
            ip_address=ip_address,
            user_agent=user_agent,
        )

        return usuario

    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.put("/{usuario_id}", response_model=UsuarioResponse)
async def update_usuario(
    usuario_id: int,
    usuario_data: UsuarioUpdate,
    request: Request,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    """Actualizar usuario"""

    try:
        ip_address, user_agent = get_client_info(request)

        usuario = UsuarioService.update(
            db=db,
            usuario_id=usuario_id,
            usuario_data=usuario_data,
            usuario_modificador_id=current_user.id,
            ip_address=ip_address,
            user_agent=user_agent,
        )

        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado"
            )

        return usuario

    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/{usuario_id}/change-password")
async def change_password(
    usuario_id: int,
    password_data: UsuarioChangePassword,
    request: Request,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    """Cambiar contraseña de usuario"""

    # Verificar que el usuario puede cambiar esta contraseña
    # (solo el mismo usuario o administrador)
    if current_user.id != usuario_id:
        # TODO: Verificar si es administrador
        pass

    try:
        ip_address, user_agent = get_client_info(request)

        success = UsuarioService.change_password(
            db=db,
            usuario_id=usuario_id,
            password_data=password_data,
            usuario_modificador_id=current_user.id,
            ip_address=ip_address,
            user_agent=user_agent,
        )

        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado"
            )

        return {"message": "Contraseña actualizada correctamente"}

    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/{usuario_id}/deactivate")
async def deactivate_usuario(
    usuario_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    """Desactivar usuario"""

    ip_address, user_agent = get_client_info(request)

    success = UsuarioService.deactivate(
        db=db,
        usuario_id=usuario_id,
        usuario_modificador_id=current_user.id,
        ip_address=ip_address,
        user_agent=user_agent,
    )

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado"
        )

    return {"message": "Usuario desactivado correctamente"}


@router.get("/{usuario_id}/historia", response_model=List[UsuarioHistoriaResponse])
async def get_usuario_historia(
    usuario_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    """Obtener historial de cambios de un usuario"""

    historia, total = UsuarioService.get_historia(
        db=db, usuario_id=usuario_id, skip=skip, limit=limit
    )

    return historia


@router.get("/historia/all", response_model=List[UsuarioHistoriaResponse])
async def get_all_historia(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    """Obtener historial completo de cambios de usuarios (solo administradores)"""

    # TODO: Verificar permisos de administrador

    historia, total = UsuarioService.get_historia(db=db, skip=skip, limit=limit)

    return historia
