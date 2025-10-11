# backend/app/api/__init__.py
from fastapi import APIRouter
from app.api import auth

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["autenticacion"])