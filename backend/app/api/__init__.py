# backend/app/api/__init__.py
from fastapi import APIRouter
from app.api import auth, usuarios, roles, menus, permisos, estados

api_router = APIRouter()

# Rutas de autenticación
api_router.include_router(auth.router, prefix="/auth", tags=["autenticacion"])

# Rutas del sistema IAM
api_router.include_router(usuarios.router, prefix="/usuarios", tags=["usuarios"])
api_router.include_router(roles.router, prefix="/roles", tags=["roles"])
api_router.include_router(menus.router, prefix="/menus", tags=["menus"])
api_router.include_router(permisos.router, prefix="/permisos", tags=["permisos"])
api_router.include_router(estados.router, prefix="/estados", tags=["estados"])