# backend/app/api/estados.py
from typing import List

from app.core.database import get_db
from app.core.security import get_current_user
from app.models import Estado, Usuario
from app.schemas.estado import EstadoCreate, EstadoResponse, EstadoUpdate
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("/", response_model=List[EstadoResponse])
async def get_estados(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    """Obtener lista de estados"""
    estados = db.query(Estado).offset(skip).limit(limit).all()
    return estados


@router.get("/{estado_id}", response_model=EstadoResponse)
async def get_estado(
    estado_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    """Obtener estado por ID"""
    estado = db.query(Estado).filter(Estado.id == estado_id).first()
    if not estado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Estado no encontrado"
        )
    return estado


@router.post("/", response_model=EstadoResponse, status_code=status.HTTP_201_CREATED)
async def create_estado(
    estado_data: EstadoCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    """Crear nuevo estado"""
    estado = Estado(**estado_data.dict())
    db.add(estado)
    db.commit()
    db.refresh(estado)
    return estado


@router.put("/{estado_id}", response_model=EstadoResponse)
async def update_estado(
    estado_id: int,
    estado_data: EstadoUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    """Actualizar estado"""
    estado = db.query(Estado).filter(Estado.id == estado_id).first()
    if not estado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Estado no encontrado"
        )

    update_data = estado_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(estado, field, value)

    db.commit()
    db.refresh(estado)
    return estado


@router.delete("/{estado_id}")
async def delete_estado(
    estado_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    """Eliminar estado"""
    estado = db.query(Estado).filter(Estado.id == estado_id).first()
    if not estado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Estado no encontrado"
        )

    db.delete(estado)
    db.commit()
    return {"message": "Estado eliminado correctamente"}
