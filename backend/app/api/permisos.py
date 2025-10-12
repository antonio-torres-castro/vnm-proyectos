# backend/app/api/permisos.py
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.models import Permiso, Usuario
from app.schemas.permiso import PermisoCreate, PermisoUpdate, PermisoResponse

router = APIRouter()

@router.get("/", response_model=List[PermisoResponse])
async def get_permisos(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Obtener lista de permisos"""
    permisos = db.query(Permiso).offset(skip).limit(limit).all()
    return permisos

@router.get("/{permiso_id}", response_model=PermisoResponse)
async def get_permiso(
    permiso_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Obtener permiso por ID"""
    permiso = db.query(Permiso).filter(Permiso.id == permiso_id).first()
    if not permiso:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Permiso no encontrado"
        )
    return permiso

@router.post("/", response_model=PermisoResponse, status_code=status.HTTP_201_CREATED)
async def create_permiso(
    permiso_data: PermisoCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Crear nuevo permiso"""
    permiso = Permiso(**permiso_data.dict())
    db.add(permiso)
    db.commit()
    db.refresh(permiso)
    return permiso

@router.put("/{permiso_id}", response_model=PermisoResponse)
async def update_permiso(
    permiso_id: int,
    permiso_data: PermisoUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Actualizar permiso"""
    permiso = db.query(Permiso).filter(Permiso.id == permiso_id).first()
    if not permiso:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Permiso no encontrado"
        )
    
    update_data = permiso_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(permiso, field, value)
    
    db.commit()
    db.refresh(permiso)
    return permiso

@router.delete("/{permiso_id}")
async def delete_permiso(
    permiso_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Eliminar permiso"""
    permiso = db.query(Permiso).filter(Permiso.id == permiso_id).first()
    if not permiso:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Permiso no encontrado"
        )
    
    db.delete(permiso)
    db.commit()
    return {"message": "Permiso eliminado correctamente"}
