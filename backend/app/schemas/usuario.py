# backend/app/schemas/usuario.py
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class UsuarioBase(BaseModel):
    email: EmailStr
    nombre_usuario: str
    rol_id: int

class UsuarioCreate(UsuarioBase):
    clave: str

class UsuarioUpdate(BaseModel):
    email: Optional[EmailStr] = None
    nombre_usuario: Optional[str] = None
    rol_id: Optional[int] = None
    estado_id: Optional[int] = None

class UsuarioResponse(UsuarioBase):
    id: int
    fecha_creacion: datetime
    estado_id: int

    class Config:
        from_attributes = True

class UsuarioLogin(BaseModel):
    email: EmailStr
    clave: str