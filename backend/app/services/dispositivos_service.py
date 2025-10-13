# backend/app/services/dispositivos_service.py
from typing import List, Tuple, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import func, desc, asc, and_, or_
from app.models.dispositivos import Dispositivos
from app.models.interfaces import Interfaces
from app.schemas.dispositivos import DispositivosFiltros


class DispositivosService:

    @staticmethod
    def get_all(
        db: Session,
        skip: int = 0,
        limit: int = 50,
        filtros: Optional[DispositivosFiltros] = None,
    ) -> Tuple[List[Dispositivos], int]:
        """Obtener dispositivos con filtros y paginación"""

        query = db.query(Dispositivos)

        # Aplicar filtros
        if filtros:
            if filtros.operador:
                query = query.filter(
                    Dispositivos.operador.ilike(f"%{filtros.operador}%")
                )

            if filtros.zona:
                query = query.filter(Dispositivos.zona.ilike(f"%{filtros.zona}%"))

            if filtros.hub:
                query = query.filter(Dispositivos.hub.ilike(f"%{filtros.hub}%"))

            if filtros.area:
                query = query.filter(Dispositivos.area.ilike(f"%{filtros.area}%"))

            if filtros.enterprise:
                query = query.filter(
                    Dispositivos.enterprise.ilike(f"%{filtros.enterprise}%")
                )

            if filtros.devstatus is not None:
                query = query.filter(Dispositivos.devstatus == filtros.devstatus)

            if filtros.solo_activos:
                query = query.filter(Dispositivos.devstatus == 1)

            if filtros.con_geolocalizacion:
                query = query.filter(
                    and_(
                        Dispositivos.latitud.isnot(None),
                        Dispositivos.longitud.isnot(None),
                    )
                )

        # Contar total
        total = query.count()

        # Aplicar paginación y ordenamiento
        dispositivos = (
            query.order_by(asc(Dispositivos.devname)).offset(skip).limit(limit).all()
        )

        return dispositivos, total

    @staticmethod
    def get_by_id(db: Session, devid: int) -> Optional[Dispositivos]:
        """Obtener dispositivo por ID"""
        return db.query(Dispositivos).filter(Dispositivos.devid == devid).first()

    @staticmethod
    def get_estadisticas(db: Session) -> Dict[str, Any]:
        """Obtener estadísticas generales de dispositivos"""

        # Estadísticas por estado
        stats_estado = (
            db.query(
                Dispositivos.devstatus, func.count(Dispositivos.devid).label("count")
            )
            .group_by(Dispositivos.devstatus)
            .all()
        )

        # Estadísticas por operador
        stats_operador = (
            db.query(
                Dispositivos.operador, func.count(Dispositivos.devid).label("count")
            )
            .filter(Dispositivos.operador.isnot(None))
            .group_by(Dispositivos.operador)
            .all()
        )

        # Estadísticas por zona
        stats_zona = (
            db.query(Dispositivos.zona, func.count(Dispositivos.devid).label("count"))
            .filter(Dispositivos.zona.isnot(None))
            .group_by(Dispositivos.zona)
            .all()
        )

        # Estadísticas por fabricante
        stats_enterprise = (
            db.query(
                Dispositivos.enterprise, func.count(Dispositivos.devid).label("count")
            )
            .filter(Dispositivos.enterprise.isnot(None))
            .group_by(Dispositivos.enterprise)
            .all()
        )

        # Calcular totales
        total_dispositivos = db.query(func.count(Dispositivos.devid)).scalar()
        dispositivos_up = (
            db.query(func.count(Dispositivos.devid))
            .filter(Dispositivos.devstatus == 1)
            .scalar()
        )
        dispositivos_down = (
            db.query(func.count(Dispositivos.devid))
            .filter(Dispositivos.devstatus == 2)
            .scalar()
        )
        dispositivos_no_responden = (
            db.query(func.count(Dispositivos.devid))
            .filter(Dispositivos.devstatus == 0)
            .scalar()
        )
        dispositivos_fuera_monitoreo = (
            db.query(func.count(Dispositivos.devid))
            .filter(Dispositivos.devstatus == 5)
            .scalar()
        )

        # Calcular porcentaje de disponibilidad
        porcentaje_disponibilidad = (
            (dispositivos_up / total_dispositivos * 100)
            if total_dispositivos > 0
            else 0
        )

        return {
            "total_dispositivos": total_dispositivos or 0,
            "dispositivos_up": dispositivos_up or 0,
            "dispositivos_down": dispositivos_down or 0,
            "dispositivos_no_responden": dispositivos_no_responden or 0,
            "dispositivos_fuera_monitoreo": dispositivos_fuera_monitoreo or 0,
            "porcentaje_disponibilidad": round(porcentaje_disponibilidad, 2),
            "por_operador": {row.operador: row.count for row in stats_operador},
            "por_zona": {row.zona: row.count for row in stats_zona},
            "por_enterprise": {row.enterprise: row.count for row in stats_enterprise},
        }

    @staticmethod
    def get_with_interfaces_count(
        db: Session,
        skip: int = 0,
        limit: int = 50,
        filtros: Optional[DispositivosFiltros] = None,
    ) -> Tuple[List[Dict], int]:
        """Obtener dispositivos con conteo de interfaces"""

        # Query base con join a interfaces
        query = (
            db.query(
                Dispositivos,
                func.count(Interfaces.id).label("interfaces_count"),
                func.sum(func.case((Interfaces.ifstatus == 1, 1), else_=0)).label(
                    "interfaces_activas"
                ),
            )
            .outerjoin(Interfaces)
            .group_by(Dispositivos.devid)
        )

        # Aplicar filtros
        if filtros:
            if filtros.operador:
                query = query.filter(
                    Dispositivos.operador.ilike(f"%{filtros.operador}%")
                )

            if filtros.zona:
                query = query.filter(Dispositivos.zona.ilike(f"%{filtros.zona}%"))

            if filtros.hub:
                query = query.filter(Dispositivos.hub.ilike(f"%{filtros.hub}%"))

            if filtros.area:
                query = query.filter(Dispositivos.area.ilike(f"%{filtros.area}%"))

            if filtros.enterprise:
                query = query.filter(
                    Dispositivos.enterprise.ilike(f"%{filtros.enterprise}%")
                )

            if filtros.devstatus is not None:
                query = query.filter(Dispositivos.devstatus == filtros.devstatus)

            if filtros.solo_activos:
                query = query.filter(Dispositivos.devstatus == 1)

            if filtros.con_geolocalizacion:
                query = query.filter(
                    and_(
                        Dispositivos.latitud.isnot(None),
                        Dispositivos.longitud.isnot(None),
                    )
                )

        # Contar total
        total = query.count()

        # Aplicar paginación
        resultados = (
            query.order_by(asc(Dispositivos.devname)).offset(skip).limit(limit).all()
        )

        # Convertir a formato de respuesta
        dispositivos_con_info = []
        for dispositivo, interfaces_count, interfaces_activas in resultados:
            dispositivos_con_info.append(
                {
                    "dispositivo": dispositivo,
                    "interfaces_count": interfaces_count or 0,
                    "interfaces_activas": interfaces_activas or 0,
                }
            )

        return dispositivos_con_info, total

    @staticmethod
    def buscar(
        db: Session, termino: str, skip: int = 0, limit: int = 50
    ) -> Tuple[List[Dispositivos], int]:
        """Buscar dispositivos por término general"""

        query = db.query(Dispositivos).filter(
            or_(
                Dispositivos.devname.ilike(f"%{termino}%"),
                Dispositivos.operador.ilike(f"%{termino}%"),
                Dispositivos.zona.ilike(f"%{termino}%"),
                Dispositivos.area.ilike(f"%{termino}%"),
                Dispositivos.enterprise.ilike(f"%{termino}%"),
                func.cast(Dispositivos.devip, db.Text).ilike(f"%{termino}%"),
            )
        )

        total = query.count()
        dispositivos = (
            query.order_by(asc(Dispositivos.devname)).offset(skip).limit(limit).all()
        )

        return dispositivos, total

    @staticmethod
    def get_valores_filtros(db: Session) -> Dict[str, List[str]]:
        """Obtener valores únicos para filtros"""

        operadores = (
            db.query(Dispositivos.operador)
            .filter(Dispositivos.operador.isnot(None))
            .distinct()
            .order_by(Dispositivos.operador)
            .all()
        )

        zonas = (
            db.query(Dispositivos.zona)
            .filter(Dispositivos.zona.isnot(None))
            .distinct()
            .order_by(Dispositivos.zona)
            .all()
        )

        hubs = (
            db.query(Dispositivos.hub)
            .filter(Dispositivos.hub.isnot(None))
            .distinct()
            .order_by(Dispositivos.hub)
            .all()
        )

        areas = (
            db.query(Dispositivos.area)
            .filter(Dispositivos.area.isnot(None))
            .distinct()
            .order_by(Dispositivos.area)
            .all()
        )

        enterprises = (
            db.query(Dispositivos.enterprise)
            .filter(Dispositivos.enterprise.isnot(None))
            .distinct()
            .order_by(Dispositivos.enterprise)
            .all()
        )

        return {
            "operadores": [row[0] for row in operadores],
            "zonas": [row[0] for row in zonas],
            "hubs": [row[0] for row in hubs],
            "areas": [row[0] for row in areas],
            "enterprises": [row[0] for row in enterprises],
        }
