# backend/app/api/roles.py
from typing import List

from app.core.database import get_db
from app.core.security import get_current_user
from app.models import Usuario
from app.schemas.menu import MenuResponse, RolMenuCreate
from app.schemas.permiso import PermisoResponse
from app.schemas.rol import (
    RolCreate,
    RolPermisoCreate,
    RolResponse,
    RolUpdate,
)
from app.services.rol_service import RolService
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("/", response_model=List[RolResponse])
async def get_roles(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    """Obtener lista de roles"""
    roles = RolService.get_all(db, skip=skip, limit=limit)
    return roles


@router.get("/{rol_id}", response_model=RolResponse)
async def get_rol(
    rol_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    """Obtener rol por ID"""
    rol = RolService.get_by_id(db, rol_id)
    if not rol:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Rol no encontrado"
        )
    return rol


@router.post("/", response_model=RolResponse, status_code=status.HTTP_201_CREATED)
async def create_rol(
    rol_data: RolCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    """Crear nuevo rol"""
    rol = RolService.create(db, rol_data)
    return rol


@router.put("/{rol_id}", response_model=RolResponse)
async def update_rol(
    rol_id: int,
    rol_data: RolUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    """Actualizar rol"""
    rol = RolService.update(db, rol_id, rol_data)
    if not rol:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Rol no encontrado"
        )
    return rol


@router.delete("/{rol_id}")
async def delete_rol(
    rol_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    """Eliminar rol"""
    success = RolService.delete(db, rol_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Rol no encontrado"
        )
    return {"message": "Rol eliminado correctamente"}


# ========== GESTIÓN DE PERMISOS ==========


@router.get("/{rol_id}/permisos", response_model=List[PermisoResponse])
async def get_rol_permisos(
    rol_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    """Obtener permisos de un rol"""
    permisos = RolService.get_permisos(db, rol_id)
    return permisos


@router.post("/{rol_id}/permisos")
async def assign_permiso_to_rol(
    rol_id: int,
    permiso_id: int,
    estado_id: int = 1,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    """Asignar permiso a rol"""
    asignacion = RolPermisoCreate(
        rol_id=rol_id, permiso_id=permiso_id, estado_id=estado_id
    )

    success = RolService.assign_permiso(db, asignacion)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error asignando permiso a rol",
        )

    return {"message": "Permiso asignado correctamente"}


@router.delete("/{rol_id}/permisos/{permiso_id}")
async def remove_permiso_from_rol(
    rol_id: int,
    permiso_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    """Remover permiso de rol"""
    success = RolService.remove_permiso(db, rol_id, permiso_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Asignación de permiso no encontrada",
        )

    return {"message": "Permiso removido correctamente"}


# ========== GESTIÓN DE MENÚS ==========


@router.get("/{rol_id}/menus", response_model=List[MenuResponse])
async def get_rol_menus(
    rol_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    """Obtener menús accesibles por un rol"""
    menus = RolService.get_menus(db, rol_id)
    return menus


@router.post("/{rol_id}/menus")
async def assign_menu_to_rol(
    rol_id: int,
    menu_id: int,
    estado_id: int = 1,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    """Asignar menú a rol"""
    asignacion = RolMenuCreate(rol_id=rol_id, menu_id=menu_id, estado_id=estado_id)

    success = RolService.assign_menu(db, asignacion)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Error asignando menú a rol"
        )

    return {"message": "Menú asignado correctamente"}


@router.delete("/{rol_id}/menus/{menu_id}")
async def remove_menu_from_rol(
    rol_id: int,
    menu_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    """Remover menú de rol"""
    success = RolService.remove_menu(db, rol_id, menu_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Asignación de menú no encontrada",
        )

    return {"message": "Menú removido correctamente"}


# ========== VERIFICACIONES DE PERMISOS ==========


@router.get("/{rol_id}/permissions/{permiso_nombre}")
async def check_permission(
    rol_id: int,
    permiso_nombre: str,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    """Verificar si un rol tiene un permiso específico"""
    has_permission = RolService.has_permission(db, rol_id, permiso_nombre)
    return {"has_permission": has_permission}


@router.get("/{rol_id}/menu-access/{menu_url:path}")
async def check_menu_access(
    rol_id: int,
    menu_url: str,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    """Verificar si un rol tiene acceso a un menú específico"""
    has_access = RolService.has_menu_access(db, rol_id, menu_url)
    return {"has_access": has_access}
