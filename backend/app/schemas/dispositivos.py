# backend/app/schemas/dispositivos.py
from pydantic import BaseModel, validator
from datetime import datetime
from typing import Optional, List
from decimal import Decimal
from ipaddress import IPv4Address

class DispositivosBase(BaseModel):
    devid: int
    operador: Optional[str] = None
    zona: Optional[str] = None
    hub: Optional[str] = None
    devip: Optional[IPv4Address] = None
    area: Optional[str] = None
    devname: Optional[str] = None
    devstatus: Optional[int] = None
    enterprise: Optional[str] = None
    modelo: Optional[str] = None
    latitud: Optional[Decimal] = None
    longitud: Optional[Decimal] = None

class DispositivosResponse(DispositivosBase):
    devstatus_lv: Optional[datetime] = None
    devstatus_lc: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Schema con información de estado interpretada
class DispositivosDetallado(DispositivosResponse):
    devstatus_nombre: Optional[str] = None
    interfaces_count: Optional[int] = None
    interfaces_activas: Optional[int] = None
    
    @validator('devstatus_nombre', pre=False, always=True)
    def get_status_name(cls, v, values):
        if 'devstatus' in values:
            status_map = {
                0: "No responde",
                1: "UP", 
                2: "Caído",
                5: "Fuera de monitoreo"
            }
            return status_map.get(values['devstatus'], "Desconocido")
        return v

# Filtros para consultas
class DispositivosFiltros(BaseModel):
    operador: Optional[str] = None
    zona: Optional[str] = None
    hub: Optional[str] = None
    area: Optional[str] = None
    enterprise: Optional[str] = None
    devstatus: Optional[int] = None
    solo_activos: Optional[bool] = False
    con_geolocalizacion: Optional[bool] = False

# Schema para listado con paginación
class DispositivosListResponse(BaseModel):
    dispositivos: List[DispositivosDetallado]
    total: int
    pagina: int
    por_pagina: int
    total_paginas: int
    filtros_aplicados: Optional[DispositivosFiltros] = None

# Schema para estadísticas
class DispositivosEstadisticas(BaseModel):
    total_dispositivos: int
    dispositivos_up: int
    dispositivos_down: int
    dispositivos_no_responden: int
    dispositivos_fuera_monitoreo: int
    porcentaje_disponibilidad: float
    por_operador: dict
    por_zona: dict
    por_enterprise: dict
