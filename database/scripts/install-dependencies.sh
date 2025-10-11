#!/bin/bash
# database/scripts/install-dependencies.sh

echo "=== Instalando dependencias del sistema ==="

# Instalar cliente PostgreSQL en contenedor backend si es necesario
docker exec monitoreo_backend apt-get update
docker exec monitoreo_backend apt-get install -y postgresql-client

# Instalar dependencias Python en contenedor backend
echo "Instalando dependencias Python..."
docker exec monitoreo_backend pip install --upgrade pip
docker exec monitoreo_backend pip install -r /app/requirements.txt

# Verificar instalación
echo "Verificando instalación..."
docker exec monitoreo_backend python -c "import fastapi; print('✅ FastAPI instalado')"
docker exec monitoreo_backend python -c "import sqlalchemy; print('✅ SQLAlchemy instalado')"
docker exec monitoreo_backend python -c "import psycopg2; print('✅ Psycopg2 instalado')"

echo "=== Dependencias instaladas correctamente ==="