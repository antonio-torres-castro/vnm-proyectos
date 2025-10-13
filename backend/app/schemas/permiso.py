# backend/app/schemas/permiso.py
from pydantic import BaseModel
from typing import Optional


class PermisoBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None


class PermisoCreate(PermisoBase):
    pass


class PermisoUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None


class PermisoResponse(PermisoBase):
    id: int

    class Config:
        from_attributes = True
