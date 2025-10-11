# backend/app/core/config.py
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "postgresql://monitoreo_user:monitoreo_pass@localhost:5432/monitoreo_dev"
    
    # JWT
    SECRET_KEY: str = "tu-clave-secreta-aqui-cambiar-en-produccion"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 540  # 9 horas
    
    # API
    API_V1_STR: str = "/api/v1"
    
    class Config:
        env_file = ".env"

settings = Settings()