# backend/app/api/__init__.py
from app.api import (
    auth,
    dispositivos,
    estados,
    interfaces,
    menus,
    permisos,
    roles,
    usuarios,
)
from fastapi import APIRouter

api_router = APIRouter()

# Rutas de autenticación
api_router.include_router(auth.router, prefix="/auth", tags=["autenticacion"])

# Rutas del sistema IAM
api_router.include_router(usuarios.router, prefix="/usuarios", tags=["usuarios"])
api_router.include_router(roles.router, prefix="/roles", tags=["roles"])
api_router.include_router(menus.router, prefix="/menus", tags=["menus"])
api_router.include_router(permisos.router, prefix="/permisos", tags=["permisos"])
api_router.include_router(estados.router, prefix="/estados", tags=["estados"])

# Rutas del sistema de Monitoreo
api_router.include_router(
    dispositivos.router,
    prefix="/monitoreo/dispositivos",
    tags=["monitoreo-dispositivos"],
)
api_router.include_router(
    interfaces.router, prefix="/monitoreo/interfaces", tags=["monitoreo-interfaces"]
)
