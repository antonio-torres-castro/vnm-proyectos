# backend/app/schemas/dispositivo_historico.py
from datetime import date, datetime
from decimal import Decimal
from typing import List, Optional

from pydantic import BaseModel, validator


class DispositivoHistoricoBase(BaseModel):
    id: int
    devid: int
    timestamp: datetime
    devstatus: Optional[int] = None
    latitud: Optional[Decimal] = None
    longitud: Optional[Decimal] = None


class DispositivoHistoricoResponse(DispositivoHistoricoBase):
    created_at: datetime

    class Config:
        from_attributes = True


# Schema con información interpretada
class DispositivoHistoricoDetallado(DispositivoHistoricoResponse):
    # Información del dispositivo
    dispositivo_nombre: Optional[str] = None
    dispositivo_area: Optional[str] = None
    dispositivo_zona: Optional[str] = None
    dispositivo_operador: Optional[str] = None

    # Estado interpretado
    devstatus_nombre: Optional[str] = None

    # Información de cambio de ubicación
    ubicacion_cambio: Optional[bool] = None
    distancia_anterior_km: Optional[float] = None

    @validator("devstatus_nombre", pre=False, always=True)
    def get_status_name(cls, v, values):
        if "devstatus" in values and values["devstatus"] is not None:
            status_map = {
                0: "No responde",
                1: "UP",
                2: "Caído",
                5: "Fuera de monitoreo",
            }
            return status_map.get(values["devstatus"], "Desconocido")
        return v


# Filtros para consultas históricas de dispositivos
class DispositivoHistoricoFiltros(BaseModel):
    devid: Optional[int] = None
    zona: Optional[str] = None
    area: Optional[str] = None
    operador: Optional[str] = None
    devstatus: Optional[int] = None
    fecha_inicio: Optional[datetime] = None
    fecha_fin: Optional[datetime] = None
    solo_cambios_estado: Optional[bool] = False
    solo_cambios_ubicacion: Optional[bool] = False


# Schema para análisis de disponibilidad
class DispositivoDisponibilidad(BaseModel):
    devid: int
    dispositivo_nombre: Optional[str] = None
    periodo_inicio: datetime
    periodo_fin: datetime

    # Métricas de disponibilidad
    tiempo_total_horas: float
    tiempo_up_horas: float
    tiempo_down_horas: float
    tiempo_no_responde_horas: float
    tiempo_fuera_monitoreo_horas: float

    # Porcentajes
    disponibilidad_pct: float
    tiempo_caido_pct: float

    # Eventos
    total_caidas: int
    caida_mas_larga_horas: Optional[float] = None
    caida_promedio_minutos: Optional[float] = None

    # SLA
    cumple_sla_99: bool
    cumple_sla_995: bool
    cumple_sla_999: bool


# Schema para eventos de cambio de estado
class DispositivoEvento(BaseModel):
    devid: int
    dispositivo_nombre: Optional[str] = None
    timestamp_inicio: datetime
    timestamp_fin: Optional[datetime] = None
    estado_anterior: Optional[int] = None
    estado_nuevo: int
    duracion_minutos: Optional[float] = None

    # Estados interpretados
    estado_anterior_nombre: Optional[str] = None
    estado_nuevo_nombre: Optional[str] = None

    @validator("estado_anterior_nombre", pre=False, always=True)
    def get_estado_anterior_name(cls, v, values):
        if "estado_anterior" in values and values["estado_anterior"] is not None:
            status_map = {
                0: "No responde",
                1: "UP",
                2: "Caído",
                5: "Fuera de monitoreo",
            }
            return status_map.get(values["estado_anterior"], "Desconocido")
        return v

    @validator("estado_nuevo_nombre", pre=False, always=True)
    def get_estado_nuevo_name(cls, v, values):
        if "estado_nuevo" in values and values["estado_nuevo"] is not None:
            status_map = {
                0: "No responde",
                1: "UP",
                2: "Caído",
                5: "Fuera de monitoreo",
            }
            return status_map.get(values["estado_nuevo"], "Desconocido")
        return v


# Schema para análisis de ubicación
class DispositivoUbicacion(BaseModel):
    devid: int
    dispositivo_nombre: Optional[str] = None
    timestamp: datetime
    latitud_anterior: Optional[Decimal] = None
    longitud_anterior: Optional[Decimal] = None
    latitud_nueva: Decimal
    longitud_nueva: Decimal
    distancia_movimiento_km: Optional[float] = None
    tipo_movimiento: Optional[str] = None  # 'menor', 'significativo', 'mayor'


# Respuesta para series temporales de estado
class DispositivoSerieEstado(BaseModel):
    devid: int
    dispositivo_nombre: Optional[str] = None
    fecha_inicio: datetime
    fecha_fin: datetime
    agregacion: str  # 'hourly', 'daily'
    datos: List[
        dict
    ]  # [{"timestamp": "...", "disponibilidad_pct": ..., "estado_predominante": ...}]


# Schema para estadísticas agregadas por período
class DispositivoEstadisticasPeriodo(BaseModel):
    periodo: str
    fecha_inicio: datetime
    fecha_fin: datetime
    total_dispositivos: int
    disponibilidad_promedio_pct: float
    dispositivos_sla_99_pct: float
    total_incidentes: int
    tiempo_promedio_resolucion_horas: Optional[float] = None
    zonas_mas_afectadas: List[dict]


# Schema para listado histórico con paginación
class DispositivoHistoricoListResponse(BaseModel):
    historico: List[DispositivoHistoricoDetallado]
    total: int
    pagina: int
    por_pagina: int
    total_paginas: int
    filtros_aplicados: Optional[DispositivoHistoricoFiltros] = None
    estadisticas_periodo: Optional[dict] = None
