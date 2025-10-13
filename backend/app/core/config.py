import os


class Settings:
    # Database - URL para Docker (usar 'postgres' como hostname)
    DATABASE_URL: str = (
        "postgresql://monitoreo_user:monitoreo_pass@postgres:5432/monitoreo_dev"
    )

    # JWT
    SECRET_KEY: str = "clave-secreta-temporal-cambiar-en-produccion"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 540  # 9 horas

    # API
    API_V1_STR: str = "/api/v1"


settings = Settings()
