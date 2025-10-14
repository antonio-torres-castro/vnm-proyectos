# backend/app/api/dispositivos.py
from typing import Optional

from app.core.database import get_db
from app.core.security import get_current_user
from app.models import Usuario
from app.schemas.dispositivos import (
    DispositivosDetallado,
    DispositivosEstadisticas,
    DispositivosFiltros,
    DispositivosListResponse,
)
from app.services.dispositivos_service import DispositivosService
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("/", response_model=DispositivosListResponse)
async def get_dispositivos(
    skip: int = Query(0, ge=0, description="Registros a omitir"),
    limit: int = Query(50, ge=1, le=100, description="Máximo registros por página"),
    operador: Optional[str] = Query(None, description="Filtrar por operador"),
    zona: Optional[str] = Query(None, description="Filtrar por zona"),
    hub: Optional[str] = Query(None, description="Filtrar por hub"),
    area: Optional[str] = Query(None, description="Filtrar por área"),
    enterprise: Optional[str] = Query(None, description="Filtrar por fabricante"),
    devstatus: Optional[int] = Query(
        None, description="Filtrar por estado del dispositivo"
    ),
    solo_activos: bool = Query(False, description="Solo dispositivos activos (UP)"),
    con_geolocalizacion: bool = Query(
        False, description="Solo dispositivos con geolocalización"
    ),
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    """Obtener lista de dispositivos con filtros y paginación"""

    # Crear objeto de filtros
    filtros = DispositivosFiltros(
        operador=operador,
        zona=zona,
        hub=hub,
        area=area,
        enterprise=enterprise,
        devstatus=devstatus,
        solo_activos=solo_activos,
        con_geolocalizacion=con_geolocalizacion,
    )

    # Obtener dispositivos con información adicional
    dispositivos_info, total = DispositivosService.get_with_interfaces_count(
        db=db, skip=skip, limit=limit, filtros=filtros
    )

    total_paginas = (total + limit - 1) // limit

    # Convertir a response detallado
    dispositivos_detallados = []
    for info in dispositivos_info:
        dispositivo = info["dispositivo"]
        dispositivo_dict = dispositivo.__dict__.copy()
        dispositivo_dict["interfaces_count"] = info["interfaces_count"]
        dispositivo_dict["interfaces_activas"] = info["interfaces_activas"]
        dispositivos_detallados.append(DispositivosDetallado(**dispositivo_dict))

    return DispositivosListResponse(
        dispositivos=dispositivos_detallados,
        total=total,
        pagina=(skip // limit) + 1,
        por_pagina=limit,
        total_paginas=total_paginas,
        filtros_aplicados=filtros,
    )


@router.get("/estadisticas", response_model=DispositivosEstadisticas)
async def get_estadisticas_dispositivos(
    db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)
):
    """Obtener estadísticas generales de dispositivos"""

    estadisticas = DispositivosService.get_estadisticas(db)

    return DispositivosEstadisticas(**estadisticas)


@router.get("/valores-filtros")
async def get_valores_filtros(
    db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)
):
    """Obtener valores únicos para filtros de dispositivos"""

    valores = DispositivosService.get_valores_filtros(db)

    return valores


@router.get("/buscar", response_model=DispositivosListResponse)
async def buscar_dispositivos(
    q: str = Query(..., min_length=2, description="Término de búsqueda"),
    skip: int = Query(0, ge=0, description="Registros a omitir"),
    limit: int = Query(50, ge=1, le=100, description="Máximo registros por página"),
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    """Buscar dispositivos por término general"""

    dispositivos, total = DispositivosService.buscar(
        db=db, termino=q, skip=skip, limit=limit
    )

    total_paginas = (total + limit - 1) // limit

    # Convertir a response detallado
    dispositivos_detallados = [
        DispositivosDetallado(**dispositivo.__dict__) for dispositivo in dispositivos
    ]

    return DispositivosListResponse(
        dispositivos=dispositivos_detallados,
        total=total,
        pagina=(skip // limit) + 1,
        por_pagina=limit,
        total_paginas=total_paginas,
    )


@router.get("/{devid}", response_model=DispositivosDetallado)
async def get_dispositivo(
    devid: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    """Obtener dispositivo específico por ID"""

    dispositivo = DispositivosService.get_by_id(db, devid)

    if not dispositivo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Dispositivo no encontrado"
        )

    # Obtener información adicional del dispositivo
    dispositivos_info, _ = DispositivosService.get_with_interfaces_count(
        db=db,
        skip=0,
        limit=1,
        filtros=DispositivosFiltros(
            devstatus=None
        ),  # Sin filtros para obtener el específico
    )

    # Buscar la info del dispositivo específico
    dispositivo_info = None
    for info in dispositivos_info:
        if info["dispositivo"].devid == devid:
            dispositivo_info = info
            break

    if dispositivo_info:
        dispositivo_dict = dispositivo_info["dispositivo"].__dict__.copy()
        dispositivo_dict["interfaces_count"] = dispositivo_info["interfaces_count"]
        dispositivo_dict["interfaces_activas"] = dispositivo_info["interfaces_activas"]
        return DispositivosDetallado(**dispositivo_dict)

    # Fallback sin información adicional
    return DispositivosDetallado(**dispositivo.__dict__)


@router.get("/zona/{zona}", response_model=DispositivosListResponse)
async def get_dispositivos_por_zona(
    zona: str,
    skip: int = Query(0, ge=0, description="Registros a omitir"),
    limit: int = Query(50, ge=1, le=100, description="Máximo registros por página"),
    solo_activos: bool = Query(False, description="Solo dispositivos activos"),
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    """Obtener dispositivos de una zona específica"""

    filtros = DispositivosFiltros(zona=zona, solo_activos=solo_activos)

    dispositivos_info, total = DispositivosService.get_with_interfaces_count(
        db=db, skip=skip, limit=limit, filtros=filtros
    )

    total_paginas = (total + limit - 1) // limit

    dispositivos_detallados = []
    for info in dispositivos_info:
        dispositivo = info["dispositivo"]
        dispositivo_dict = dispositivo.__dict__.copy()
        dispositivo_dict["interfaces_count"] = info["interfaces_count"]
        dispositivo_dict["interfaces_activas"] = info["interfaces_activas"]
        dispositivos_detallados.append(DispositivosDetallado(**dispositivo_dict))

    return DispositivosListResponse(
        dispositivos=dispositivos_detallados,
        total=total,
        pagina=(skip // limit) + 1,
        por_pagina=limit,
        total_paginas=total_paginas,
        filtros_aplicados=filtros,
    )


@router.get("/geolocalizados/mapa")
async def get_dispositivos_mapa(
    solo_activos: bool = Query(False, description="Solo dispositivos activos"),
    zona: Optional[str] = Query(None, description="Filtrar por zona"),
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    """Obtener dispositivos con geolocalización para visualización en mapa"""

    filtros = DispositivosFiltros(
        zona=zona, solo_activos=solo_activos, con_geolocalizacion=True
    )

    # Obtener todos los dispositivos geolocalizados (sin paginación para mapa)
    dispositivos, total = DispositivosService.get_all(
        db=db, skip=0, limit=10000, filtros=filtros  # Límite alto para mapa
    )

    # Formatear para mapa
    dispositivos_mapa = []
    for dispositivo in dispositivos:
        dispositivos_mapa.append(
            {
                "devid": dispositivo.devid,
                "devname": dispositivo.devname,
                "zona": dispositivo.zona,
                "area": dispositivo.area,
                "devstatus": dispositivo.devstatus,
                "devstatus_nombre": {
                    0: "No responde",
                    1: "UP",
                    2: "Caído",
                    5: "Fuera de monitoreo",
                }.get(dispositivo.devstatus, "Desconocido"),
                "latitud": float(dispositivo.latitud),
                "longitud": float(dispositivo.longitud),
                "enterprise": dispositivo.enterprise,
                "modelo": dispositivo.modelo,
            }
        )

    return {"total": total, "dispositivos": dispositivos_mapa}
