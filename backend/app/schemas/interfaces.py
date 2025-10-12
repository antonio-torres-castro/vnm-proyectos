# backend/app/schemas/interfaces.py
from pydantic import BaseModel, validator
from datetime import datetime
from typing import Optional, List
from decimal import Decimal

class InterfacesBase(BaseModel):
    id: int
    devid: int
    devif: int
    ifname: Optional[str] = None
    ifalias: Optional[str] = None
    ifadmin: Optional[int] = None
    ifoper: Optional[int] = None
    ifstatus: Optional[int] = None
    ifgraficar: Optional[int] = None
    ifspeed: Optional[int] = None

class InterfacesResponse(InterfacesBase):
    iflv: Optional[datetime] = None
    iflc: Optional[datetime] = None
    time: Optional[datetime] = None
    input: Optional[int] = None
    output: Optional[int] = None
    ifindis: Optional[int] = None
    ifoutdis: Optional[int] = None
    ifinerr: Optional[int] = None
    ifouterr: Optional[int] = None
    ifutil: Optional[Decimal] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Schema con información interpretada y cálculos
class InterfacesDetallado(InterfacesResponse):
    # Información del dispositivo padre
    dispositivo_nombre: Optional[str] = None
    dispositivo_area: Optional[str] = None
    dispositivo_zona: Optional[str] = None
    
    # Estados interpretados
    ifadmin_nombre: Optional[str] = None
    ifoper_nombre: Optional[str] = None
    ifstatus_nombre: Optional[str] = None
    ifgraficar_nombre: Optional[str] = None
    
    # Métricas calculadas
    input_mbps: Optional[float] = None
    output_mbps: Optional[float] = None
    total_mbps: Optional[float] = None
    input_percentage: Optional[float] = None
    output_percentage: Optional[float] = None
    
    @validator('ifadmin_nombre', pre=False, always=True)
    def get_ifadmin_name(cls, v, values):
        if 'ifadmin' in values and values['ifadmin'] is not None:
            return "Up" if values['ifadmin'] == 1 else "Down"
        return v

    @validator('ifoper_nombre', pre=False, always=True)
    def get_ifoper_name(cls, v, values):
        if 'ifoper' in values and values['ifoper'] is not None:
            return "Up" if values['ifoper'] == 1 else "Down"
        return v

    @validator('ifstatus_nombre', pre=False, always=True)
    def get_ifstatus_name(cls, v, values):
        if 'ifstatus' in values and values['ifstatus'] is not None:
            status_map = {
                1: "UP",
                2: "Down", 
                3: "Shutdown"
            }
            return status_map.get(values['ifstatus'], "Desconocido")
        return v

    @validator('ifgraficar_nombre', pre=False, always=True)
    def get_ifgraficar_name(cls, v, values):
        if 'ifgraficar' in values and values['ifgraficar'] is not None:
            return "En monitoreo" if values['ifgraficar'] == 1 else "Sin monitoreo"
        return v

    @validator('input_mbps', pre=False, always=True)
    def calc_input_mbps(cls, v, values):
        if 'input' in values and values['input'] is not None:
            return round(values['input'] / 1_000_000, 2)  # bps to Mbps
        return v

    @validator('output_mbps', pre=False, always=True)
    def calc_output_mbps(cls, v, values):
        if 'output' in values and values['output'] is not None:
            return round(values['output'] / 1_000_000, 2)  # bps to Mbps
        return v

    @validator('total_mbps', pre=False, always=True)
    def calc_total_mbps(cls, v, values):
        input_mbps = values.get('input_mbps', 0) or 0
        output_mbps = values.get('output_mbps', 0) or 0
        return round(input_mbps + output_mbps, 2)

    @validator('input_percentage', pre=False, always=True)
    def calc_input_percentage(cls, v, values):
        if ('input' in values and values['input'] is not None and 
            'ifspeed' in values and values['ifspeed'] is not None and values['ifspeed'] > 0):
            input_mbps = values['input'] / 1_000_000
            speed_mbps = values['ifspeed']
            return round((input_mbps / speed_mbps) * 100, 2)
        return v

    @validator('output_percentage', pre=False, always=True)
    def calc_output_percentage(cls, v, values):
        if ('output' in values and values['output'] is not None and 
            'ifspeed' in values and values['ifspeed'] is not None and values['ifspeed'] > 0):
            output_mbps = values['output'] / 1_000_000
            speed_mbps = values['ifspeed']
            return round((output_mbps / speed_mbps) * 100, 2)
        return v

# Filtros para consultas
class InterfacesFiltros(BaseModel):
    devid: Optional[int] = None
    zona: Optional[str] = None
    area: Optional[str] = None
    ifstatus: Optional[int] = None
    ifgraficar: Optional[int] = None
    solo_activas: Optional[bool] = False
    solo_monitoreadas: Optional[bool] = False
    utilization_min: Optional[float] = None
    utilization_max: Optional[float] = None
    speed_min: Optional[int] = None
    speed_max: Optional[int] = None

# Schema para listado con paginación
class InterfacesListResponse(BaseModel):
    interfaces: List[InterfacesDetallado]
    total: int
    pagina: int
    por_pagina: int
    total_paginas: int
    filtros_aplicados: Optional[InterfacesFiltros] = None

# Schema para métricas agregadas
class InterfacesMetricas(BaseModel):
    total_interfaces: int
    interfaces_up: int
    interfaces_down: int
    interfaces_shutdown: int
    interfaces_monitoreadas: int
    utilization_promedio: Optional[float] = None
    top_utilizadas: List[InterfacesDetallado]
    con_errores: int
    con_descartes: int
