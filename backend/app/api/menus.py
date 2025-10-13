# backend/app/api/menus.py
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.services.menu_service import MenuService
from app.schemas.menu import (
    MenuCreate, MenuUpdate, MenuResponse, MenuConGrupo,
    MenuGrupoCreate, MenuGrupoUpdate, MenuGrupoResponse, MenuGrupoConMenus
)
from app.models import Usuario

router = APIRouter()

# ========== GESTIÓN DE GRUPOS DE MENÚ ==========

@router.get("/grupos", response_model=List[MenuGrupoConMenus])
async def get_menu_grupos(
    activos_solo: bool = Query(True, description="Solo grupos activos"),
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Obtener todos los grupos de menú"""
    grupos = MenuService.get_all_grupos(db, activos_solo=activos_solo)
    return grupos

@router.get("/grupos/{grupo_id}", response_model=MenuGrupoResponse)
async def get_menu_grupo(
    grupo_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Obtener grupo de menú por ID"""
    grupo = MenuService.get_grupo_by_id(db, grupo_id)
    if not grupo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Grupo de menú no encontrado"
        )
    return grupo

@router.post("/grupos", response_model=MenuGrupoResponse, status_code=status.HTTP_201_CREATED)
async def create_menu_grupo(
    grupo_data: MenuGrupoCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Crear nuevo grupo de menú"""
    grupo = MenuService.create_grupo(db, grupo_data)
    return grupo

@router.put("/grupos/{grupo_id}", response_model=MenuGrupoResponse)
async def update_menu_grupo(
    grupo_id: int,
    grupo_data: MenuGrupoUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Actualizar grupo de menú"""
    grupo = MenuService.update_grupo(db, grupo_id, grupo_data)
    if not grupo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Grupo de menú no encontrado"
        )
    return grupo

# ========== GESTIÓN DE MENÚS ==========

@router.get("/", response_model=List[MenuConGrupo])
async def get_menus(
    grupo_id: Optional[int] = Query(None, description="Filtrar por grupo"),
    activos_solo: bool = Query(True, description="Solo menús activos"),
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Obtener todos los menús"""
    menus = MenuService.get_all_menus(db, grupo_id=grupo_id, activos_solo=activos_solo)
    return menus

@router.get("/{menu_id}", response_model=MenuConGrupo)
async def get_menu(
    menu_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Obtener menú por ID"""
    menu = MenuService.get_menu_by_id(db, menu_id)
    if not menu:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Menú no encontrado"
        )
    return menu

@router.post("/", response_model=MenuResponse, status_code=status.HTTP_201_CREATED)
async def create_menu(
    menu_data: MenuCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Crear nuevo menú"""
    menu = MenuService.create_menu(db, menu_data)
    return menu

@router.put("/{menu_id}", response_model=MenuResponse)
async def update_menu(
    menu_id: int,
    menu_data: MenuUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Actualizar menú"""
    menu = MenuService.update_menu(db, menu_id, menu_data)
    if not menu:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Menú no encontrado"
        )
    return menu

# ========== ESTRUCTURA DE MENÚS ==========

@router.get("/tree/all")
async def get_menu_tree(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Obtener estructura completa de menús"""
    tree = MenuService.get_menu_tree(db)
    return {"menu_tree": tree}

@router.get("/tree/role/{rol_id}")
async def get_menu_tree_by_role(
    rol_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Obtener estructura de menús accesible por rol"""
    tree = MenuService.get_menu_tree(db, rol_id=rol_id)
    return {"menu_tree": tree}

@router.get("/tree/my-role")
async def get_my_menu_tree(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Obtener estructura de menús para el usuario actual"""
    tree = MenuService.get_menu_tree(db, rol_id=current_user.rol_id)
    return {"menu_tree": tree}

# ========== REORDENAMIENTO ==========

@router.post("/reorder")
async def reorder_menus(
    menu_orders: List[dict],
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Reordenar menús

    Body: [{"id": 1, "orden": 1}, {"id": 2, "orden": 2}, ...]
    """
    success = MenuService.reorder_menus(db, menu_orders)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error reordenando menús"
        )

    return {"message": "Menús reordenados correctamente"}

@router.post("/grupos/reorder")
async def reorder_grupos(
    grupo_orders: List[dict],
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Reordenar grupos de menú

    Body: [{"id": 1, "orden": 1}, {"id": 2, "orden": 2}, ...]
    """
    success = MenuService.reorder_grupos(db, grupo_orders)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error reordenando grupos"
        )

    return {"message": "Grupos reordenados correctamente"}
