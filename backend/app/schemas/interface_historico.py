# backend/app/schemas/interface_historico.py
from datetime import date, datetime
from decimal import Decimal
from typing import List, Optional

from pydantic import BaseModel, validator


class InterfaceHistoricoBase(BaseModel):
    id: int
    devif: int
    timestamp: datetime
    input: Optional[int] = None
    output: Optional[int] = None
    ifspeed: Optional[int] = None
    ifindis: Optional[int] = None
    ifoutdis: Optional[int] = None
    ifinerr: Optional[int] = None
    ifouterr: Optional[int] = None
    ifutil: Optional[Decimal] = None


class InterfaceHistoricoResponse(InterfaceHistoricoBase):
    created_at: datetime

    class Config:
        from_attributes = True


# Schema con información calculada
class InterfaceHistoricoDetallado(InterfaceHistoricoResponse):
    # Información de la interface y dispositivo
    interface_name: Optional[str] = None
    dispositivo_nombre: Optional[str] = None
    dispositivo_area: Optional[str] = None

    # Métricas calculadas en Mbps
    input_mbps: Optional[float] = None
    output_mbps: Optional[float] = None
    total_mbps: Optional[float] = None

    @validator("input_mbps", pre=False, always=True)
    def calc_input_mbps(cls, v, values):
        if "input" in values and values["input"] is not None:
            return round(values["input"] / 1_000_000, 2)
        return v

    @validator("output_mbps", pre=False, always=True)
    def calc_output_mbps(cls, v, values):
        if "output" in values and values["output"] is not None:
            return round(values["output"] / 1_000_000, 2)
        return v

    @validator("total_mbps", pre=False, always=True)
    def calc_total_mbps(cls, v, values):
        input_mbps = values.get("input_mbps", 0) or 0
        output_mbps = values.get("output_mbps", 0) or 0
        return round(input_mbps + output_mbps, 2)


# Filtros para consultas históricas
class InterfaceHistoricoFiltros(BaseModel):
    devif: Optional[int] = None
    fecha_inicio: Optional[datetime] = None
    fecha_fin: Optional[datetime] = None
    solo_con_datos: Optional[bool] = True
    intervalo_minutos: Optional[int] = None  # Para agregación temporal


# Parámetros para consultas de series temporales
class SerieTemporalRequest(BaseModel):
    devif: int
    fecha_inicio: datetime
    fecha_fin: datetime
    metrica: str  # 'input', 'output', 'ifutil', 'ifinerr', etc.
    agregacion: Optional[str] = "raw"  # 'raw', 'hourly', 'daily'
    incluir_nulos: Optional[bool] = False


# Respuesta de serie temporal
class SerieTemporalResponse(BaseModel):
    devif: int
    metrica: str
    agregacion: str
    fecha_inicio: datetime
    fecha_fin: datetime
    total_puntos: int
    datos: List[dict]  # [{"timestamp": "...", "valor": ...}, ...]


# Schema para datos agregados por período
class InterfaceHistoricoAgregado(BaseModel):
    devif: int
    periodo: str  # 'hourly', 'daily', 'weekly'
    timestamp: datetime
    input_promedio: Optional[float] = None
    input_maximo: Optional[int] = None
    input_minimo: Optional[int] = None
    output_promedio: Optional[float] = None
    output_maximo: Optional[int] = None
    output_minimo: Optional[int] = None
    ifutil_promedio: Optional[float] = None
    ifutil_maximo: Optional[Decimal] = None
    errores_total: Optional[int] = None
    descartes_total: Optional[int] = None
    muestras_count: int


# Schema para análisis de tendencias
class InterfaceTendencias(BaseModel):
    devif: int
    interface_name: Optional[str] = None
    dispositivo_nombre: Optional[str] = None
    periodo_analisis: str
    fecha_inicio: datetime
    fecha_fin: datetime

    # Tendencias de tráfico
    trafico_promedio_mbps: Optional[float] = None
    trafico_pico_mbps: Optional[float] = None
    crecimiento_trafico_pct: Optional[float] = None

    # Tendencias de utilización
    utilizacion_promedio_pct: Optional[float] = None
    utilizacion_pico_pct: Optional[float] = None

    # Calidad de enlace
    errores_promedio_por_hora: Optional[float] = None
    descartes_promedio_por_hora: Optional[float] = None
    disponibilidad_pct: Optional[float] = None


# Schema para listado histórico con paginación
class InterfaceHistoricoListResponse(BaseModel):
    historico: List[InterfaceHistoricoDetallado]
    total: int
    pagina: int
    por_pagina: int
    total_paginas: int
    filtros_aplicados: Optional[InterfaceHistoricoFiltros] = None
    resumen_periodo: Optional[dict] = None
