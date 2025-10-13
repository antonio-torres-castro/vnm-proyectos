# backend/app/schemas/estado.py
from typing import Optional

from pydantic import BaseModel


class EstadoBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None


class EstadoCreate(EstadoBase):
    pass


class EstadoUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None


class EstadoResponse(EstadoBase):
    id: int

    class Config:
        from_attributes = True
