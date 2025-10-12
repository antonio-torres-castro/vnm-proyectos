# backend/app/api/interfaces.py
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.services.interfaces_service import InterfacesService
from app.schemas.interfaces import (
    InterfacesResponse, InterfacesDetallado, InterfacesListResponse,
    InterfacesFiltros, InterfacesMetricas
)
from app.models import Usuario

router = APIRouter()

@router.get("/", response_model=InterfacesListResponse)
async def get_interfaces(
    skip: int = Query(0, ge=0, description="Registros a omitir"),
    limit: int = Query(50, ge=1, le=100, description="Máximo registros por página"),
    devid: Optional[int] = Query(None, description="Filtrar por ID de dispositivo"),
    zona: Optional[str] = Query(None, description="Filtrar por zona"),
    area: Optional[str] = Query(None, description="Filtrar por área"),
    ifstatus: Optional[int] = Query(None, description="Filtrar por estado de interface"),
    ifgraficar: Optional[int] = Query(None, description="Filtrar por monitoreo (0=No, 1=Sí)"),
    solo_activas: bool = Query(False, description="Solo interfaces activas (UP)"),
    solo_monitoreadas: bool = Query(False, description="Solo interfaces monitoreadas"),
    utilization_min: Optional[float] = Query(None, ge=0, le=100, description="Utilización mínima (%)"),
    utilization_max: Optional[float] = Query(None, ge=0, le=100, description="Utilización máxima (%)"),
    speed_min: Optional[int] = Query(None, ge=0, description="Velocidad mínima (Mbps)"),
    speed_max: Optional[int] = Query(None, ge=0, description="Velocidad máxima (Mbps)"),
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Obtener lista de interfaces con filtros y paginación"""
    
    # Crear objeto de filtros
    filtros = InterfacesFiltros(
        devid=devid,
        zona=zona,
        area=area,
        ifstatus=ifstatus,
        ifgraficar=ifgraficar,
        solo_activas=solo_activas,
        solo_monitoreadas=solo_monitoreadas,
        utilization_min=utilization_min,
        utilization_max=utilization_max,
        speed_min=speed_min,
        speed_max=speed_max
    )
    
    interfaces, total = InterfacesService.get_all(
        db=db, 
        skip=skip, 
        limit=limit,
        filtros=filtros
    )
    
    total_paginas = (total + limit - 1) // limit
    
    # Convertir a response detallado con información adicional
    interfaces_detalladas = []
    for interface in interfaces:
        interface_dict = interface.__dict__.copy()
        # Agregar información del dispositivo
        if interface.dispositivo:
            interface_dict["dispositivo_nombre"] = interface.dispositivo.devname
            interface_dict["dispositivo_area"] = interface.dispositivo.area
            interface_dict["dispositivo_zona"] = interface.dispositivo.zona
        
        interfaces_detalladas.append(InterfacesDetallado(**interface_dict))
    
    return InterfacesListResponse(
        interfaces=interfaces_detalladas,
        total=total,
        pagina=(skip // limit) + 1,
        por_pagina=limit,
        total_paginas=total_paginas,
        filtros_aplicados=filtros
    )

@router.get("/metricas", response_model=InterfacesMetricas)
async def get_metricas_interfaces(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Obtener métricas generales de interfaces"""
    
    metricas = InterfacesService.get_metricas(db)
    
    # Convertir top_utilizadas a formato detallado
    top_utilizadas_detalladas = []
    for interface in metricas["top_utilizadas"]:
        interface_dict = interface.__dict__.copy()
        if interface.dispositivo:
            interface_dict["dispositivo_nombre"] = interface.dispositivo.devname
            interface_dict["dispositivo_area"] = interface.dispositivo.area
            interface_dict["dispositivo_zona"] = interface.dispositivo.zona
        top_utilizadas_detalladas.append(InterfacesDetallado(**interface_dict))
    
    metricas["top_utilizadas"] = top_utilizadas_detalladas
    
    return InterfacesMetricas(**metricas)

@router.get("/alta-utilizacion", response_model=InterfacesListResponse)
async def get_interfaces_alta_utilizacion(
    threshold: float = Query(80.0, ge=0, le=100, description="Umbral de utilización (%)"),
    skip: int = Query(0, ge=0, description="Registros a omitir"),
    limit: int = Query(50, ge=1, le=100, description="Máximo registros por página"),
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Obtener interfaces con alta utilización"""
    
    interfaces, total = InterfacesService.get_high_utilization(
        db=db,
        threshold=threshold,
        skip=skip,
        limit=limit
    )
    
    total_paginas = (total + limit - 1) // limit
    
    interfaces_detalladas = []
    for interface in interfaces:
        interface_dict = interface.__dict__.copy()
        if interface.dispositivo:
            interface_dict["dispositivo_nombre"] = interface.dispositivo.devname
            interface_dict["dispositivo_area"] = interface.dispositivo.area
            interface_dict["dispositivo_zona"] = interface.dispositivo.zona
        interfaces_detalladas.append(InterfacesDetallado(**interface_dict))
    
    return InterfacesListResponse(
        interfaces=interfaces_detalladas,
        total=total,
        pagina=(skip // limit) + 1,
        por_pagina=limit,
        total_paginas=total_paginas
    )

@router.get("/con-errores", response_model=InterfacesListResponse)
async def get_interfaces_con_errores(
    skip: int = Query(0, ge=0, description="Registros a omitir"),
    limit: int = Query(50, ge=1, le=100, description="Máximo registros por página"),
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Obtener interfaces con errores"""
    
    interfaces, total = InterfacesService.get_with_errors(
        db=db,
        skip=skip,
        limit=limit
    )
    
    total_paginas = (total + limit - 1) // limit
    
    interfaces_detalladas = []
    for interface in interfaces:
        interface_dict = interface.__dict__.copy()
        if interface.dispositivo:
            interface_dict["dispositivo_nombre"] = interface.dispositivo.devname
            interface_dict["dispositivo_area"] = interface.dispositivo.area
            interface_dict["dispositivo_zona"] = interface.dispositivo.zona
        interfaces_detalladas.append(InterfacesDetallado(**interface_dict))
    
    return InterfacesListResponse(
        interfaces=interfaces_detalladas,
        total=total,
        pagina=(skip // limit) + 1,
        por_pagina=limit,
        total_paginas=total_paginas
    )

@router.get("/buscar", response_model=InterfacesListResponse)
async def buscar_interfaces(
    q: str = Query(..., min_length=2, description="Término de búsqueda"),
    skip: int = Query(0, ge=0, description="Registros a omitir"),
    limit: int = Query(50, ge=1, le=100, description="Máximo registros por página"),
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Buscar interfaces por término general"""
    
    interfaces, total = InterfacesService.buscar(
        db=db,
        termino=q,
        skip=skip,
        limit=limit
    )
    
    total_paginas = (total + limit - 1) // limit
    
    interfaces_detalladas = []
    for interface in interfaces:
        interface_dict = interface.__dict__.copy()
        if interface.dispositivo:
            interface_dict["dispositivo_nombre"] = interface.dispositivo.devname
            interface_dict["dispositivo_area"] = interface.dispositivo.area
            interface_dict["dispositivo_zona"] = interface.dispositivo.zona
        interfaces_detalladas.append(InterfacesDetallado(**interface_dict))
    
    return InterfacesListResponse(
        interfaces=interfaces_detalladas,
        total=total,
        pagina=(skip // limit) + 1,
        por_pagina=limit,
        total_paginas=total_paginas
    )

@router.get("/estadisticas-zona")
async def get_estadisticas_por_zona(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Obtener estadísticas de interfaces agrupadas por zona"""
    
    estadisticas = InterfacesService.get_estadisticas_por_zona(db)
    
    return estadisticas

@router.get("/por-velocidad", response_model=InterfacesListResponse)
async def get_interfaces_por_velocidad(
    speed_min: int = Query(..., ge=0, description="Velocidad mínima (Mbps)"),
    speed_max: int = Query(..., ge=0, description="Velocidad máxima (Mbps)"),
    skip: int = Query(0, ge=0, description="Registros a omitir"),
    limit: int = Query(50, ge=1, le=100, description="Máximo registros por página"),
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Obtener interfaces por rango de velocidad"""
    
    if speed_min > speed_max:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La velocidad mínima no puede ser mayor que la máxima"
        )
    
    interfaces, total = InterfacesService.get_by_speed_range(
        db=db,
        speed_min=speed_min,
        speed_max=speed_max,
        skip=skip,
        limit=limit
    )
    
    total_paginas = (total + limit - 1) // limit
    
    interfaces_detalladas = []
    for interface in interfaces:
        interface_dict = interface.__dict__.copy()
        if interface.dispositivo:
            interface_dict["dispositivo_nombre"] = interface.dispositivo.devname
            interface_dict["dispositivo_area"] = interface.dispositivo.area
            interface_dict["dispositivo_zona"] = interface.dispositivo.zona
        interfaces_detalladas.append(InterfacesDetallado(**interface_dict))
    
    return InterfacesListResponse(
        interfaces=interfaces_detalladas,
        total=total,
        pagina=(skip // limit) + 1,
        por_pagina=limit,
        total_paginas=total_paginas
    )

@router.get("/{interface_id}", response_model=InterfacesDetallado)
async def get_interface(
    interface_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Obtener interface específica por ID"""
    
    interface = InterfacesService.get_by_id(db, interface_id)
    
    if not interface:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Interface no encontrada"
        )
    
    interface_dict = interface.__dict__.copy()
    if interface.dispositivo:
        interface_dict["dispositivo_nombre"] = interface.dispositivo.devname
        interface_dict["dispositivo_area"] = interface.dispositivo.area
        interface_dict["dispositivo_zona"] = interface.dispositivo.zona
    
    return InterfacesDetallado(**interface_dict)

@router.get("/dispositivo/{devid}", response_model=InterfacesListResponse)
async def get_interfaces_por_dispositivo(
    devid: int,
    skip: int = Query(0, ge=0, description="Registros a omitir"),
    limit: int = Query(50, ge=1, le=100, description="Máximo registros por página"),
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Obtener interfaces de un dispositivo específico"""
    
    interfaces, total = InterfacesService.get_by_dispositivo(
        db=db,
        devid=devid,
        skip=skip,
        limit=limit
    )
    
    total_paginas = (total + limit - 1) // limit
    
    interfaces_detalladas = []
    for interface in interfaces:
        interface_dict = interface.__dict__.copy()
        if interface.dispositivo:
            interface_dict["dispositivo_nombre"] = interface.dispositivo.devname
            interface_dict["dispositivo_area"] = interface.dispositivo.area
            interface_dict["dispositivo_zona"] = interface.dispositivo.zona
        interfaces_detalladas.append(InterfacesDetallado(**interface_dict))
    
    return InterfacesListResponse(
        interfaces=interfaces_detalladas,
        total=total,
        pagina=(skip // limit) + 1,
        por_pagina=limit,
        total_paginas=total_paginas
    )
