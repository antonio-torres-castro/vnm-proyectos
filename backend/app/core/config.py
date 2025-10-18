import os


class Settings:
    # Database - Para desarrollo local (solo DB en Docker)
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql://monitoreo_user:monitoreo_pass@localhost:5432/monitoreo_dev"
    )

    # JWT - Lee desde variables de entorno Docker
    SECRET_KEY: str = os.getenv(
        "SECRET_KEY", 
        "clave-secreta-temporal-cambiar-en-produccion"
    )
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(
        os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "540")
    )

    # API
    API_V1_STR: str = "/api/v1"


settings = Settings()
