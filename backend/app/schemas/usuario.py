# backend/app/schemas/usuario.py
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, validator


class UsuarioBase(BaseModel):
    email: EmailStr
    nombre_usuario: str
    rol_id: int


class UsuarioCreate(UsuarioBase):
    clave: str
    fecha_inicio: Optional[datetime] = None
    fecha_termino: Optional[datetime] = None
    estado_id: Optional[int] = 1  # Activo por defecto

    @validator("clave")
    def validate_password(cls, v):
        if len(v) < 6:
            raise ValueError("La contraseña debe tener al menos 6 caracteres")
        return v


class UsuarioUpdate(BaseModel):
    email: Optional[EmailStr] = None
    nombre_usuario: Optional[str] = None
    rol_id: Optional[int] = None
    estado_id: Optional[int] = None
    fecha_inicio: Optional[datetime] = None
    fecha_termino: Optional[datetime] = None


class UsuarioChangePassword(BaseModel):
    clave_actual: str
    clave_nueva: str
    confirmar_clave: str

    @validator("clave_nueva")
    def validate_new_password(cls, v):
        if len(v) < 6:
            raise ValueError("La contraseña debe tener al menos 6 caracteres")
        return v

    @validator("confirmar_clave")
    def passwords_match(cls, v, values):
        if "clave_nueva" in values and v != values["clave_nueva"]:
            raise ValueError("Las contraseñas no coinciden")
        return v


class UsuarioResponse(UsuarioBase):
    id: int
    fecha_creacion: datetime
    fecha_inicio: Optional[datetime]
    fecha_termino: Optional[datetime]
    fecha_modificacion: datetime
    estado_id: int

    class Config:
        from_attributes = True


# Schema con información relacionada
class UsuarioDetallado(UsuarioResponse):
    rol_nombre: Optional[str] = None
    estado_nombre: Optional[str] = None


class UsuarioLogin(BaseModel):
    email: EmailStr
    clave: str


# Schema para listado con paginación
class UsuarioListResponse(BaseModel):
    usuarios: list[UsuarioResponse]
    total: int
    pagina: int
    por_pagina: int
    total_paginas: int
