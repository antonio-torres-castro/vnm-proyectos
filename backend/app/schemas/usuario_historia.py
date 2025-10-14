# backend/app/schemas/usuario_historia.py
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class UsuarioHistoriaBase(BaseModel):
    usuario_id: Optional[int] = None
    rol_id: Optional[int] = None
    email: Optional[str] = None
    nombre_usuario: Optional[str] = None
    estado_id: Optional[int] = None


class UsuarioHistoriaCreate(UsuarioHistoriaBase):
    clave_hash: Optional[str] = None  # Solo para auditoría, sin mostrar


class UsuarioHistoriaResponse(BaseModel):
    id: int
    usuario_id: Optional[int]
    rol_id: Optional[int]
    email: Optional[str]
    nombre_usuario: Optional[str]
    estado_id: Optional[int]
    fecha: datetime

    class Config:
        from_attributes = True


# Schema extendido con información relacionada
class UsuarioHistoriaDetallada(UsuarioHistoriaResponse):
    rol_nombre: Optional[str] = None
    estado_nombre: Optional[str] = None
