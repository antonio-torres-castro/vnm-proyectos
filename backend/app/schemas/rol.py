# backend/app/schemas/rol.py
from pydantic import BaseModel
from typing import Optional, List, TYPE_CHECKING
from datetime import datetime

if TYPE_CHECKING:
    from app.schemas.permiso import PermisoResponse

class RolBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None

class RolCreate(RolBase):
    pass

class RolUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None

class RolResponse(RolBase):
    id: int

    class Config:
        from_attributes = True

# Schema con permisos incluidos
class RolConPermisos(RolResponse):
    permisos: List['PermisoResponse'] = []

# Schema para asignación de permisos
class RolPermisoCreate(BaseModel):
    rol_id: int
    permiso_id: int
    estado_id: Optional[int] = 1  # Activo por defecto

class RolPermisoResponse(BaseModel):
    rol_id: int
    permiso_id: int
    estado_id: Optional[int]
    fecha_creacion: datetime
    fecha_modificacion: datetime

    class Config:
        from_attributes = True
