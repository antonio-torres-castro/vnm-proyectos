#!/usr/bin/env python3
"""
Script de correccion de compatibilidad para contenedores VNM
Corrige problemas de versiones en backend y frontend para desarrollo

PROBLEMA 1: Backend - FastAPI/Pydantic incompatibles  
PROBLEMA 2: Frontend - Node.js obsoleto y comando Vite invalido
PROBLEMA 3: Healthchecks - curl no disponible

Compatible con Windows PowerShell
Ubicacion: vnm-proyectos\automate\fix_containers_compatibility.py
"""

import os
import sys
import shutil
import json
from datetime import datetime
from pathlib import Path

def log_accion(mensaje):
    """Log de acciones realizadas"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"[{timestamp}] {mensaje}")

def crear_backup(archivo_path, sufijo="_backup"):
    """Crear backup de archivo antes de modificar"""
    backup_path = f"{archivo_path}{sufijo}"
    try:
        shutil.copy2(archivo_path, backup_path)
        log_accion(f"BACKUP creado: {backup_path}")
        return backup_path
    except Exception as e:
        log_accion(f"ERROR creando backup de {archivo_path}: {e}")
        return None

def verificar_archivo_existe(archivo_path):
    """Verificar que archivo existe"""
    if not os.path.exists(archivo_path):
        log_accion(f"ERROR: Archivo no encontrado: {archivo_path}")
        return False
    return True

def actualizar_backend_requirements():
    """Actualizar backend/requirements.txt con versiones compatibles"""
    log_accion("INICIANDO: Actualizacion backend requirements.txt")
    
    archivo_path = "backend/requirements.txt"
    if not verificar_archivo_existe(archivo_path):
        return False
    
    # Crear backup
    if not crear_backup(archivo_path):
        return False
    
    # Contenido actualizado con versiones compatibles
    nuevo_contenido = """# FastAPI core - Versiones compatibles actualizadas
fastapi==0.115.4
uvicorn[standard]==0.32.0

# Database
sqlalchemy==2.0.23
psycopg2-binary==2.9.11

# Authentication & Security
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
bcrypt==4.0.1

# Validation & Models - Version fija para compatibilidad
pydantic==2.9.2
email-validator==2.0.0

# Utilities
python-dotenv==1.0.0
python-multipart==0.0.6

# Development
debugpy==1.8.0
"""
    
    try:
        with open(archivo_path, 'w', encoding='utf-8') as f:
            f.write(nuevo_contenido)
        log_accion("EXITO: backend/requirements.txt actualizado")
        log_accion("  - FastAPI: 0.104.1 -> 0.115.4")
        log_accion("  - Uvicorn: 0.24.0 -> 0.32.0") 
        log_accion("  - Pydantic: sin version -> 2.9.2 (fija)")
        return True
    except Exception as e:
        log_accion(f"ERROR actualizando backend/requirements.txt: {e}")
        return False

def actualizar_backend_dockerfile():
    """Actualizar backend/Dockerfile.dev para agregar curl"""
    log_accion("INICIANDO: Actualizacion backend Dockerfile.dev")
    
    archivo_path = "backend/Dockerfile.dev"
    if not verificar_archivo_existe(archivo_path):
        return False
    
    # Crear backup
    if not crear_backup(archivo_path):
        return False
    
    try:
        with open(archivo_path, 'r', encoding='utf-8') as f:
            contenido = f.read()
        
        # Reemplazar la seccion de apt-get para incluir curl
        contenido_viejo = """RUN apt-get update && apt-get install -y \\
    build-essential \\
    libffi-dev \\
    libssl-dev \\
    && rm -rf /var/lib/apt/lists/*"""
    
        contenido_nuevo = """RUN apt-get update && apt-get install -y \\
    build-essential \\
    libffi-dev \\
    libssl-dev \\
    curl \\
    && rm -rf /var/lib/apt/lists/*"""
        
        contenido_actualizado = contenido.replace(contenido_viejo, contenido_nuevo)
        
        with open(archivo_path, 'w', encoding='utf-8') as f:
            f.write(contenido_actualizado)
        
        log_accion("EXITO: backend/Dockerfile.dev actualizado")
        log_accion("  - Agregado: curl para healthcheck")
        return True
        
    except Exception as e:
        log_accion(f"ERROR actualizando backend/Dockerfile.dev: {e}")
        return False

def actualizar_frontend_package_json():
    """Actualizar frontend/package.json para corregir comando Vite"""
    log_accion("INICIANDO: Actualizacion frontend package.json")
    
    archivo_path = "frontend/package.json"
    if not verificar_archivo_existe(archivo_path):
        return False
    
    # Crear backup
    if not crear_backup(archivo_path):
        return False
    
    try:
        with open(archivo_path, 'r', encoding='utf-8') as f:
            package_data = json.load(f)
        
        # Corregir script dev:debug removiendo parametro invalido --sourcemap
        if 'scripts' in package_data and 'dev:debug' in package_data['scripts']:
            package_data['scripts']['dev:debug'] = "vite --host 0.0.0.0 --mode development"
            log_accion("  - Corregido: dev:debug script (removido --sourcemap invalido)")
        
        # Escribir archivo actualizado con formato bonito
        with open(archivo_path, 'w', encoding='utf-8') as f:
            json.dump(package_data, f, indent=4, ensure_ascii=False)
        
        log_accion("EXITO: frontend/package.json actualizado")
        return True
        
    except Exception as e:
        log_accion(f"ERROR actualizando frontend/package.json: {e}")
        return False

def actualizar_frontend_dockerfile():
    """Actualizar frontend/Dockerfile.dev para usar Node.js 22"""
    log_accion("INICIANDO: Actualizacion frontend Dockerfile.dev")
    
    archivo_path = "frontend/Dockerfile.dev"
    if not verificar_archivo_existe(archivo_path):
        return False
    
    # Crear backup
    if not crear_backup(archivo_path):
        return False
    
    try:
        with open(archivo_path, 'r', encoding='utf-8') as f:
            contenido = f.read()
        
        # Actualizar version de Node.js
        contenido_actualizado = contenido.replace(
            "FROM node:18-alpine",
            "FROM node:22-alpine"
        )
        
        # Agregar curl para healthcheck si no esta
        if "curl" not in contenido_actualizado:
            # Agregar instalacion de curl despues de WORKDIR
            lineas = contenido_actualizado.split('\n')
            for i, linea in enumerate(lineas):
                if linea.strip() == "WORKDIR /app":
                    lineas.insert(i + 1, "")
                    lineas.insert(i + 2, "# Instalar curl para healthcheck")
                    lineas.insert(i + 3, "RUN apk add --no-cache curl")
                    break
            contenido_actualizado = '\n'.join(lineas)
        
        with open(archivo_path, 'w', encoding='utf-8') as f:
            f.write(contenido_actualizado)
        
        log_accion("EXITO: frontend/Dockerfile.dev actualizado")
        log_accion("  - Node.js: 18-alpine -> 22-alpine")
        log_accion("  - Agregado: curl para healthcheck")
        return True
        
    except Exception as e:
        log_accion(f"ERROR actualizando frontend/Dockerfile.dev: {e}")
        return False

def validar_cambios():
    """Validar que los cambios se aplicaron correctamente"""
    log_accion("INICIANDO: Validacion de cambios aplicados")
    
    validaciones = []
    
    # Validar backend requirements.txt
    try:
        with open("backend/requirements.txt", 'r', encoding='utf-8') as f:
            contenido = f.read()
            if "fastapi==0.115.4" in contenido and "pydantic==2.9.2" in contenido:
                validaciones.append("VALIDO: backend requirements.txt")
            else:
                validaciones.append("ERROR: backend requirements.txt - versiones incorrectas")
    except:
        validaciones.append("ERROR: No se pudo leer backend requirements.txt")
    
    # Validar backend Dockerfile.dev
    try:
        with open("backend/Dockerfile.dev", 'r', encoding='utf-8') as f:
            contenido = f.read()
            if "curl" in contenido:
                validaciones.append("VALIDO: backend Dockerfile.dev")
            else:
                validaciones.append("ERROR: backend Dockerfile.dev - curl no encontrado")
    except:
        validaciones.append("ERROR: No se pudo leer backend Dockerfile.dev")
    
    # Validar frontend package.json
    try:
        with open("frontend/package.json", 'r', encoding='utf-8') as f:
            package_data = json.load(f)
            script_debug = package_data.get('scripts', {}).get('dev:debug', '')
            if "--sourcemap" not in script_debug and "--mode development" in script_debug:
                validaciones.append("VALIDO: frontend package.json")
            else:
                validaciones.append("ERROR: frontend package.json - script dev:debug incorrecto")
    except:
        validaciones.append("ERROR: No se pudo leer frontend package.json")
    
    # Validar frontend Dockerfile.dev
    try:
        with open("frontend/Dockerfile.dev", 'r', encoding='utf-8') as f:
            contenido = f.read()
            if "node:22-alpine" in contenido and "curl" in contenido:
                validaciones.append("VALIDO: frontend Dockerfile.dev")
            else:
                validaciones.append("ERROR: frontend Dockerfile.dev - Node.js 22 o curl no encontrado")
    except:
        validaciones.append("ERROR: No se pudo leer frontend Dockerfile.dev")
    
    # Mostrar resultados de validacion
    log_accion("RESULTADOS DE VALIDACION:")
    for resultado in validaciones:
        log_accion(f"  {resultado}")
    
    errores = [v for v in validaciones if v.startswith("ERROR")]
    return len(errores) == 0

def main():
    """Funcion principal"""
    log_accion("="*60)
    log_accion("SCRIPT DE CORRECCION DE COMPATIBILIDAD VNM")
    log_accion("="*60)
    
    # Verificar que estemos en el directorio correcto
    if not os.path.exists("backend") or not os.path.exists("frontend"):
        log_accion("ERROR: Ejecute desde directorio vnm-proyectos")
        sys.exit(1)
    
    exitos = 0
    total = 4
    
    # Ejecutar correcciones
    if actualizar_backend_requirements():
        exitos += 1
    
    if actualizar_backend_dockerfile():
        exitos += 1
    
    if actualizar_frontend_package_json():
        exitos += 1
    
    if actualizar_frontend_dockerfile():
        exitos += 1
    
    log_accion("="*60)
    log_accion(f"RESUMEN: {exitos}/{total} correcciones aplicadas")
    
    if exitos == total:
        if validar_cambios():
            log_accion("EXITO TOTAL: Todas las correcciones aplicadas y validadas")
            log_accion("")
            log_accion("SIGUIENTE PASO:")
            log_accion("1. Reconstruir contenedores: python automate/vnm_automate.py dev-restart")
            log_accion("2. Verificar que todos los servicios esten healthy")
        else:
            log_accion("ADVERTENCIA: Correcciones aplicadas pero validacion fallo")
    else:
        log_accion("ERROR: No todas las correcciones se aplicaron correctamente")
        sys.exit(1)

if __name__ == "__main__":
    main()