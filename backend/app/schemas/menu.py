# backend/app/schemas/menu.py
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


# Esquemas para MenuGrupo
class MenuGrupoBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    icono: Optional[str] = None
    orden: Optional[int] = 0
    nombre_despliegue: Optional[str] = None
    estado_id: Optional[int] = 1


class MenuGrupoCreate(MenuGrupoBase):
    pass


class MenuGrupoUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    icono: Optional[str] = None
    orden: Optional[int] = None
    nombre_despliegue: Optional[str] = None
    estado_id: Optional[int] = None


class MenuGrupoResponse(MenuGrupoBase):
    id: int
    fecha_creacion: datetime
    fecha_modificacion: datetime

    class Config:
        from_attributes = True


# Esquemas para Menu
class MenuBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    url: Optional[str] = None
    icono: Optional[str] = None
    orden: Optional[int] = 0
    nombre_despliegue: Optional[str] = None
    menu_grupo_id: int
    estado_id: Optional[int] = 1


class MenuCreate(MenuBase):
    pass


class MenuUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    url: Optional[str] = None
    icono: Optional[str] = None
    orden: Optional[int] = None
    nombre_despliegue: Optional[str] = None
    menu_grupo_id: Optional[int] = None
    estado_id: Optional[int] = None


class MenuResponse(MenuBase):
    id: int
    fecha_creacion: datetime
    fecha_modificacion: datetime

    class Config:
        from_attributes = True


# Schema para menús con grupo incluido
class MenuConGrupo(MenuResponse):
    grupo: MenuGrupoResponse


# Schema para grupo con menus incluidos
class MenuGrupoConMenus(MenuGrupoResponse):
    menus: List[MenuResponse] = []


# Schema para asignación de menús a roles
class RolMenuCreate(BaseModel):
    rol_id: int
    menu_id: int
    estado_id: Optional[int] = 1


class RolMenuResponse(BaseModel):
    rol_id: int
    menu_id: int
    estado_id: Optional[int]
    fecha_creacion: datetime
    fecha_modificacion: datetime

    class Config:
        from_attributes = True
