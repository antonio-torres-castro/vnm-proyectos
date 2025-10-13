# backend/app/services/interfaces_service.py
from typing import List, Tuple, Optional, Dict, Any
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, desc, asc, and_, or_
from app.models.interfaces import Interfaces
from app.models.dispositivos import Dispositivos
from app.schemas.interfaces import InterfacesFiltros

class InterfacesService:

    @staticmethod
    def get_all(
        db: Session,
        skip: int = 0,
        limit: int = 50,
        filtros: Optional[InterfacesFiltros] = None
    ) -> Tuple[List[Interfaces], int]:
        """Obtener interfaces con filtros y paginación"""

        query = db.query(Interfaces).options(joinedload(Interfaces.dispositivo))

        # Aplicar filtros
        if filtros:
            if filtros.devid:
                query = query.filter(Interfaces.devid == filtros.devid)

            if filtros.zona:
                query = query.join(Dispositivos).filter(Dispositivos.zona.ilike(f"%{filtros.zona}%"))

            if filtros.area:
                query = query.join(Dispositivos).filter(Dispositivos.area.ilike(f"%{filtros.area}%"))

            if filtros.ifstatus is not None:
                query = query.filter(Interfaces.ifstatus == filtros.ifstatus)

            if filtros.ifgraficar is not None:
                query = query.filter(Interfaces.ifgraficar == filtros.ifgraficar)

            if filtros.solo_activas:
                query = query.filter(Interfaces.ifstatus == 1)

            if filtros.solo_monitoreadas:
                query = query.filter(Interfaces.ifgraficar == 1)

            if filtros.utilization_min is not None:
                query = query.filter(Interfaces.ifutil >= filtros.utilization_min)

            if filtros.utilization_max is not None:
                query = query.filter(Interfaces.ifutil <= filtros.utilization_max)

            if filtros.speed_min is not None:
                query = query.filter(Interfaces.ifspeed >= filtros.speed_min)

            if filtros.speed_max is not None:
                query = query.filter(Interfaces.ifspeed <= filtros.speed_max)

        # Contar total
        total = query.count()

        # Aplicar paginación y ordenamiento
        interfaces = query.order_by(asc(Interfaces.devid), asc(Interfaces.devif)).offset(skip).limit(limit).all()

        return interfaces, total

    @staticmethod
    def get_by_id(db: Session, interface_id: int) -> Optional[Interfaces]:
        """Obtener interface por ID"""
        return db.query(Interfaces).options(joinedload(Interfaces.dispositivo)).filter(Interfaces.id == interface_id).first()

    @staticmethod
    def get_by_devif(db: Session, devif: int) -> Optional[Interfaces]:
        """Obtener interface por DEVIF"""
        return db.query(Interfaces).options(joinedload(Interfaces.dispositivo)).filter(Interfaces.devif == devif).first()

    @staticmethod
    def get_by_dispositivo(
        db: Session,
        devid: int,
        skip: int = 0,
        limit: int = 50
    ) -> Tuple[List[Interfaces], int]:
        """Obtener interfaces de un dispositivo específico"""

        query = db.query(Interfaces).filter(Interfaces.devid == devid)

        total = query.count()
        interfaces = query.order_by(asc(Interfaces.devif)).offset(skip).limit(limit).all()

        return interfaces, total

    @staticmethod
    def get_metricas(db: Session) -> Dict[str, Any]:
        """Obtener métricas generales de interfaces"""

        # Estadísticas por estado
        stats_estado = db.query(
            Interfaces.ifstatus,
            func.count(Interfaces.id).label('count')
        ).group_by(Interfaces.ifstatus).all()

        # Contadores básicos
        total_interfaces = db.query(func.count(Interfaces.id)).scalar()
        interfaces_up = db.query(func.count(Interfaces.id)).filter(Interfaces.ifstatus == 1).scalar()
        interfaces_down = db.query(func.count(Interfaces.id)).filter(Interfaces.ifstatus == 2).scalar()
        interfaces_shutdown = db.query(func.count(Interfaces.id)).filter(Interfaces.ifstatus == 3).scalar()
        interfaces_monitoreadas = db.query(func.count(Interfaces.id)).filter(Interfaces.ifgraficar == 1).scalar()

        # Utilización promedio
        utilizacion_promedio = db.query(func.avg(Interfaces.ifutil)).filter(
            and_(
                Interfaces.ifutil.isnot(None),
                Interfaces.ifgraficar == 1
            )
        ).scalar()

        # Interfaces con errores
        con_errores = db.query(func.count(Interfaces.id)).filter(
            or_(
                and_(Interfaces.ifinerr.isnot(None), Interfaces.ifinerr > 0),
                and_(Interfaces.ifouterr.isnot(None), Interfaces.ifouterr > 0)
            )
        ).scalar()

        # Interfaces con descartes
        con_descartes = db.query(func.count(Interfaces.id)).filter(
            or_(
                and_(Interfaces.ifindis.isnot(None), Interfaces.ifindis > 0),
                and_(Interfaces.ifoutdis.isnot(None), Interfaces.ifoutdis > 0)
            )
        ).scalar()

        # Top 10 interfaces más utilizadas
        top_utilizadas = db.query(Interfaces).options(joinedload(Interfaces.dispositivo)).filter(
            and_(
                Interfaces.ifutil.isnot(None),
                Interfaces.ifgraficar == 1
            )
        ).order_by(desc(Interfaces.ifutil)).limit(10).all()

        return {
            "total_interfaces": total_interfaces or 0,
            "interfaces_up": interfaces_up or 0,
            "interfaces_down": interfaces_down or 0,
            "interfaces_shutdown": interfaces_shutdown or 0,
            "interfaces_monitoreadas": interfaces_monitoreadas or 0,
            "utilizacion_promedio": round(float(utilizacion_promedio), 2) if utilizacion_promedio else 0,
            "con_errores": con_errores or 0,
            "con_descartes": con_descartes or 0,
            "top_utilizadas": top_utilizadas
        }

    @staticmethod
    def get_high_utilization(
        db: Session,
        threshold: float = 80.0,
        skip: int = 0,
        limit: int = 50
    ) -> Tuple[List[Interfaces], int]:
        """Obtener interfaces con alta utilización"""

        query = db.query(Interfaces).options(joinedload(Interfaces.dispositivo)).filter(
            and_(
                Interfaces.ifutil >= threshold,
                Interfaces.ifgraficar == 1
            )
        )

        total = query.count()
        interfaces = query.order_by(desc(Interfaces.ifutil)).offset(skip).limit(limit).all()

        return interfaces, total

    @staticmethod
    def get_with_errors(
        db: Session,
        skip: int = 0,
        limit: int = 50
    ) -> Tuple[List[Interfaces], int]:
        """Obtener interfaces con errores"""

        query = db.query(Interfaces).options(joinedload(Interfaces.dispositivo)).filter(
            or_(
                and_(Interfaces.ifinerr.isnot(None), Interfaces.ifinerr > 0),
                and_(Interfaces.ifouterr.isnot(None), Interfaces.ifouterr > 0)
            )
        )

        total = query.count()
        interfaces = query.order_by(desc(Interfaces.ifinerr + Interfaces.ifouterr)).offset(skip).limit(limit).all()

        return interfaces, total

    @staticmethod
    def buscar(
        db: Session,
        termino: str,
        skip: int = 0,
        limit: int = 50
    ) -> Tuple[List[Interfaces], int]:
        """Buscar interfaces por término general"""

        query = db.query(Interfaces).options(joinedload(Interfaces.dispositivo)).filter(
            or_(
                Interfaces.ifname.ilike(f"%{termino}%"),
                Interfaces.ifalias.ilike(f"%{termino}%"),
                func.cast(Interfaces.devif, db.Text).ilike(f"%{termino}%")
            )
        )

        total = query.count()
        interfaces = query.order_by(asc(Interfaces.devid), asc(Interfaces.devif)).offset(skip).limit(limit).all()

        return interfaces, total

    @staticmethod
    def get_estadisticas_por_zona(db: Session) -> Dict[str, Any]:
        """Obtener estadísticas de interfaces agrupadas por zona"""

        stats = db.query(
            Dispositivos.zona,
            func.count(Interfaces.id).label('total_interfaces'),
            func.sum(
                func.case(
                    (Interfaces.ifstatus == 1, 1),
                    else_=0
                )
            ).label('interfaces_up'),
            func.avg(Interfaces.ifutil).label('utilizacion_promedio')
        ).join(Dispositivos).filter(
            Dispositivos.zona.isnot(None)
        ).group_by(Dispositivos.zona).all()

        return {
            row.zona: {
                "total_interfaces": row.total_interfaces,
                "interfaces_up": row.interfaces_up or 0,
                "utilizacion_promedio": round(float(row.utilizacion_promedio), 2) if row.utilizacion_promedio else 0
            }
            for row in stats
        }

    @staticmethod
    def get_by_speed_range(
        db: Session,
        speed_min: int,
        speed_max: int,
        skip: int = 0,
        limit: int = 50
    ) -> Tuple[List[Interfaces], int]:
        """Obtener interfaces por rango de velocidad"""

        query = db.query(Interfaces).options(joinedload(Interfaces.dispositivo)).filter(
            and_(
                Interfaces.ifspeed >= speed_min,
                Interfaces.ifspeed <= speed_max
            )
        )

        total = query.count()
        interfaces = query.order_by(desc(Interfaces.ifspeed)).offset(skip).limit(limit).all()

        return interfaces, total
