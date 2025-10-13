# backend/app/schemas/usuario_historia.py
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class UsuarioHistoriaBase(BaseModel):
    usuario_id: int
    rol_id: Optional[int] = None
    email: str
    nombre_usuario: str
    estado_id: Optional[int] = None
    accion: str  # CREATE, UPDATE, DELETE
    usuario_modificador_id: Optional[int] = None
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None


class UsuarioHistoriaCreate(UsuarioHistoriaBase):
    clave_hash: Optional[str] = None  # Solo para auditoría, sin mostrar


class UsuarioHistoriaResponse(BaseModel):
    id: int
    usuario_id: int
    rol_id: Optional[int]
    email: str
    nombre_usuario: str
    estado_id: Optional[int]
    fecha: datetime
    accion: str
    usuario_modificador_id: Optional[int]
    ip_address: Optional[str]
    user_agent: Optional[str]

    class Config:
        from_attributes = True


# Schema extendido con información relacionada
class UsuarioHistoriaDetallada(UsuarioHistoriaResponse):
    rol_nombre: Optional[str] = None
    estado_nombre: Optional[str] = None
    usuario_modificador_nombre: Optional[str] = None
