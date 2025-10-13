# backend/app/services/menu_service.py
from typing import Optional, List
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_
from app.models import Menu, MenuGrupo, RolMenu
from app.schemas.menu import MenuCreate, MenuUpdate, MenuGrupoCreate, MenuGrupoUpdate


class MenuService:

    # ========== GESTIÓN DE GRUPOS DE MENÚ ==========

    @staticmethod
    def get_grupo_by_id(db: Session, grupo_id: int) -> Optional[MenuGrupo]:
        """Obtener grupo de menú por ID"""
        return db.query(MenuGrupo).filter(MenuGrupo.id == grupo_id).first()

    @staticmethod
    def get_all_grupos(db: Session, activos_solo: bool = True) -> List[MenuGrupo]:
        """Obtener todos los grupos de menú"""
        query = db.query(MenuGrupo).options(joinedload(MenuGrupo.menus))

        if activos_solo:
            query = query.filter(MenuGrupo.estado_id == 1)

        return query.order_by(MenuGrupo.orden).all()

    @staticmethod
    def create_grupo(db: Session, grupo_data: MenuGrupoCreate) -> MenuGrupo:
        """Crear nuevo grupo de menú"""
        db_grupo = MenuGrupo(**grupo_data.dict())
        db.add(db_grupo)
        db.commit()
        db.refresh(db_grupo)
        return db_grupo

    @staticmethod
    def update_grupo(
        db: Session, grupo_id: int, grupo_data: MenuGrupoUpdate
    ) -> Optional[MenuGrupo]:
        """Actualizar grupo de menú"""
        db_grupo = MenuService.get_grupo_by_id(db, grupo_id)
        if not db_grupo:
            return None

        update_data = grupo_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_grupo, field, value)

        db.commit()
        db.refresh(db_grupo)
        return db_grupo

    # ========== GESTIÓN DE MENÚS ==========

    @staticmethod
    def get_menu_by_id(db: Session, menu_id: int) -> Optional[Menu]:
        """Obtener menú por ID"""
        return (
            db.query(Menu)
            .options(joinedload(Menu.grupo))
            .filter(Menu.id == menu_id)
            .first()
        )

    @staticmethod
    def get_all_menus(
        db: Session, grupo_id: Optional[int] = None, activos_solo: bool = True
    ) -> List[Menu]:
        """Obtener todos los menús"""
        query = db.query(Menu).options(joinedload(Menu.grupo))

        if grupo_id:
            query = query.filter(Menu.menu_grupo_id == grupo_id)

        if activos_solo:
            query = query.filter(Menu.estado_id == 1)

        return query.order_by(Menu.orden).all()

    @staticmethod
    def create_menu(db: Session, menu_data: MenuCreate) -> Menu:
        """Crear nuevo menú"""
        db_menu = Menu(**menu_data.dict())
        db.add(db_menu)
        db.commit()
        db.refresh(db_menu)
        return db_menu

    @staticmethod
    def update_menu(db: Session, menu_id: int, menu_data: MenuUpdate) -> Optional[Menu]:
        """Actualizar menú"""
        db_menu = MenuService.get_menu_by_id(db, menu_id)
        if not db_menu:
            return None

        update_data = menu_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_menu, field, value)

        db.commit()
        db.refresh(db_menu)
        return db_menu

    @staticmethod
    def get_menus_by_role(db: Session, rol_id: int) -> List[MenuGrupo]:
        """Obtener estructura de menús accesibles por rol"""
        # Obtener todos los grupos
        grupos = (
            db.query(MenuGrupo)
            .filter(MenuGrupo.estado_id == 1)
            .order_by(MenuGrupo.orden)
            .all()
        )

        # Para cada grupo, obtener menús accesibles
        for grupo in grupos:
            menus_accesibles = (
                db.query(Menu)
                .join(RolMenu)
                .filter(
                    and_(
                        Menu.menu_grupo_id == grupo.id,
                        Menu.estado_id == 1,
                        RolMenu.rol_id == rol_id,
                        RolMenu.estado_id == 1,
                    )
                )
                .order_by(Menu.orden)
                .all()
            )

            # Asignar menús accesibles al grupo
            grupo.menus_accesibles = menus_accesibles

        # Filtrar grupos que tienen al menos un menú accesible
        grupos_con_menus = [
            grupo
            for grupo in grupos
            if hasattr(grupo, "menus_accesibles") and grupo.menus_accesibles
        ]

        return grupos_con_menus

    @staticmethod
    def get_menu_tree(db: Session, rol_id: Optional[int] = None) -> List[dict]:
        """Obtener árbol de menús en formato jerárquico"""
        if rol_id:
            grupos = MenuService.get_menus_by_role(db, rol_id)
        else:
            grupos = MenuService.get_all_grupos(db)

        menu_tree = []
        for grupo in grupos:
            grupo_dict = {
                "id": grupo.id,
                "nombre": grupo.nombre,
                "nombre_despliegue": grupo.nombre_despliegue,
                "icono": grupo.icono,
                "orden": grupo.orden,
                "menus": [],
            }

            # Obtener menús del grupo
            if rol_id and hasattr(grupo, "menus_accesibles"):
                menus = grupo.menus_accesibles
            else:
                menus = MenuService.get_all_menus(db, grupo_id=grupo.id)

            for menu in menus:
                menu_dict = {
                    "id": menu.id,
                    "nombre": menu.nombre,
                    "nombre_despliegue": menu.nombre_despliegue,
                    "url": menu.url,
                    "icono": menu.icono,
                    "orden": menu.orden,
                }
                grupo_dict["menus"].append(menu_dict)

            if grupo_dict["menus"]:  # Solo incluir grupos con menús
                menu_tree.append(grupo_dict)

        return menu_tree

    @staticmethod
    def reorder_menus(db: Session, menu_orders: List[dict]) -> bool:
        """Reordenar menús

        Args:
            menu_orders: Lista de {"id": int, "orden": int}
        """
        try:
            for item in menu_orders:
                menu = db.query(Menu).filter(Menu.id == item["id"]).first()
                if menu:
                    menu.orden = item["orden"]

            db.commit()
            return True
        except Exception:
            db.rollback()
            return False

    @staticmethod
    def reorder_grupos(db: Session, grupo_orders: List[dict]) -> bool:
        """Reordenar grupos de menú

        Args:
            grupo_orders: Lista de {"id": int, "orden": int}
        """
        try:
            for item in grupo_orders:
                grupo = db.query(MenuGrupo).filter(MenuGrupo.id == item["id"]).first()
                if grupo:
                    grupo.orden = item["orden"]

            db.commit()
            return True
        except Exception:
            db.rollback()
            return False
