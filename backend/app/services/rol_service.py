# backend/app/services/rol_service.py
from typing import Optional, List
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_
from app.models import Rol, RolPermiso, RolMenu, Permiso, Menu
from app.schemas.rol import RolCreate, RolUpdate, RolPermisoCreate
from app.schemas.menu import RolMenuCreate


class RolService:

    @staticmethod
    def get_by_id(db: Session, rol_id: int) -> Optional[Rol]:
        """Obtener rol por ID"""
        return db.query(Rol).filter(Rol.id == rol_id).first()

    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100) -> List[Rol]:
        """Obtener todos los roles"""
        return db.query(Rol).offset(skip).limit(limit).all()

    @staticmethod
    def create(db: Session, rol_data: RolCreate) -> Rol:
        """Crear nuevo rol"""
        db_rol = Rol(**rol_data.dict())
        db.add(db_rol)
        db.commit()
        db.refresh(db_rol)
        return db_rol

    @staticmethod
    def update(db: Session, rol_id: int, rol_data: RolUpdate) -> Optional[Rol]:
        """Actualizar rol"""
        db_rol = RolService.get_by_id(db, rol_id)
        if not db_rol:
            return None

        update_data = rol_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_rol, field, value)

        db.commit()
        db.refresh(db_rol)
        return db_rol

    @staticmethod
    def delete(db: Session, rol_id: int) -> bool:
        """Eliminar rol"""
        db_rol = RolService.get_by_id(db, rol_id)
        if not db_rol:
            return False

        db.delete(db_rol)
        db.commit()
        return True

    # ========== GESTIÓN DE PERMISOS ==========

    @staticmethod
    def get_permisos(db: Session, rol_id: int) -> List[Permiso]:
        """Obtener permisos de un rol"""
        return (
            db.query(Permiso)
            .join(RolPermiso)
            .filter(
                and_(RolPermiso.rol_id == rol_id, RolPermiso.estado_id == 1)  # Activo
            )
            .all()
        )

    @staticmethod
    def assign_permiso(db: Session, asignacion: RolPermisoCreate) -> bool:
        """Asignar permiso a rol"""
        # Verificar si ya existe la asignación
        existing = (
            db.query(RolPermiso)
            .filter(
                and_(
                    RolPermiso.rol_id == asignacion.rol_id,
                    RolPermiso.permiso_id == asignacion.permiso_id,
                )
            )
            .first()
        )

        if existing:
            # Actualizar estado si existe
            existing.estado_id = asignacion.estado_id
        else:
            # Crear nueva asignación
            db_asignacion = RolPermiso(**asignacion.dict())
            db.add(db_asignacion)

        db.commit()
        return True

    @staticmethod
    def remove_permiso(db: Session, rol_id: int, permiso_id: int) -> bool:
        """Remover permiso de rol"""
        asignacion = (
            db.query(RolPermiso)
            .filter(
                and_(RolPermiso.rol_id == rol_id, RolPermiso.permiso_id == permiso_id)
            )
            .first()
        )

        if not asignacion:
            return False

        db.delete(asignacion)
        db.commit()
        return True

    # ========== GESTIÓN DE MENÚS ==========

    @staticmethod
    def get_menus(db: Session, rol_id: int) -> List[Menu]:
        """Obtener menús accesibles por un rol"""
        return (
            db.query(Menu)
            .join(RolMenu)
            .filter(and_(RolMenu.rol_id == rol_id, RolMenu.estado_id == 1))  # Activo
            .order_by(Menu.orden)
            .all()
        )

    @staticmethod
    def assign_menu(db: Session, asignacion: RolMenuCreate) -> bool:
        """Asignar menú a rol"""
        # Verificar si ya existe la asignación
        existing = (
            db.query(RolMenu)
            .filter(
                and_(
                    RolMenu.rol_id == asignacion.rol_id,
                    RolMenu.menu_id == asignacion.menu_id,
                )
            )
            .first()
        )

        if existing:
            # Actualizar estado si existe
            existing.estado_id = asignacion.estado_id
        else:
            # Crear nueva asignación
            db_asignacion = RolMenu(**asignacion.dict())
            db.add(db_asignacion)

        db.commit()
        return True

    @staticmethod
    def remove_menu(db: Session, rol_id: int, menu_id: int) -> bool:
        """Remover menú de rol"""
        asignacion = (
            db.query(RolMenu)
            .filter(and_(RolMenu.rol_id == rol_id, RolMenu.menu_id == menu_id))
            .first()
        )

        if not asignacion:
            return False

        db.delete(asignacion)
        db.commit()
        return True

    @staticmethod
    def has_permission(db: Session, rol_id: int, permiso_nombre: str) -> bool:
        """Verificar si un rol tiene un permiso específico"""
        return (
            db.query(RolPermiso)
            .join(Permiso)
            .filter(
                and_(
                    RolPermiso.rol_id == rol_id,
                    RolPermiso.estado_id == 1,
                    Permiso.nombre == permiso_nombre,
                )
            )
            .first()
            is not None
        )

    @staticmethod
    def has_menu_access(db: Session, rol_id: int, menu_url: str) -> bool:
        """Verificar si un rol tiene acceso a un menú específico"""
        return (
            db.query(RolMenu)
            .join(Menu)
            .filter(
                and_(
                    RolMenu.rol_id == rol_id,
                    RolMenu.estado_id == 1,
                    Menu.url == menu_url,
                    Menu.estado_id == 1,
                )
            )
            .first()
            is not None
        )
