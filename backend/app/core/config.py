# backend/app/core/config.py
import os
from typing import Optional

class Settings:
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://monitoreo_user:monitoreo_pass@db:5432/monitoreo_dev")
    
    # JWT
    SECRET_KEY: str = os.getenv("SECRET_KEY", "clave-secreta-temporal-cambiar-en-produccion")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 540  # 9 horas
    
    # API
    API_V1_STR: str = "/api/v1"

settings = Settings()