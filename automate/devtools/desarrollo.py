#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Acceso Rapido para Desarrollo VNM-Proyectos
=====================================================

Comandos simplificados para las operaciones mas comunes.

Uso:
    python desarrollo.py              # Diagnosticar
    python desarrollo.py up           # Iniciar entorno
    python desarrollo.py down         # Terminar entorno
    python desarrollo.py restart      # Reiniciar entorno
    python desarrollo.py clean        # Limpieza completa
    python desarrollo.py logs [servicio]  # Ver logs

Autor: MiniMax Agent
"""

import sys
import subprocess
from pathlib import Path


def ejecutar_orquestador(args):
    """Ejecutar el orquestador principal con argumentos"""
    orquestador_path = Path(__file__).parent / "orquestador_desarrollo.py"
    cmd = [sys.executable, str(orquestador_path)] + args
    # Cambiar al directorio padre (raiz del proyecto) para ejecutar el orquestador
    proyecto_root = Path(__file__).parent.parent
    return subprocess.run(cmd, cwd=proyecto_root).returncode


def mostrar_logs(servicio=None):
    """Mostrar logs de servicios"""
    if servicio:
        # Mapear nombres simples a nombres de contenedores
        contenedores = {
            'backend': 'vnm_backend_debug',
            'frontend': 'vnm_frontend_debug',
            'postgres': 'vnm_postgres_debug',
            'db': 'vnm_postgres_debug'
        }
        
        contenedor = contenedores.get(servicio, servicio)
        cmd = ['docker', 'logs', '-f', contenedor]
    else:
        cmd = ['docker-compose', '-f', '../docker-compose.debug.yml', 'logs', '-f']
    
    return subprocess.run(cmd).returncode


def mostrar_ayuda():
    """Mostrar ayuda de comandos"""
    print("""
[START] Comandos de Desarrollo VNM-Proyectos
========================================

Comandos basicos:
  python vnm.py              Diagnosticar estado
  python vnm.py up           Iniciar entorno completo
  python vnm.py down         Terminar entorno (con backup)
  python vnm.py restart      Reiniciar entorno
  python vnm.py clean        Limpieza completa + regenerar

Comandos de logs:
  python vnm.py logs         Ver todos los logs
  python vnm.py logs backend Ver logs del backend
  python vnm.py logs postgres Ver logs de PostgreSQL
  
Comandos avanzados:
  python vnm.py diagnosticar Diagnostico detallado
  python vnm.py backup       Crear backup manual
  python vnm.py regenerar    Regenerar completamente

URLs despues de iniciar:
  - Frontend:     http://localhost:3000
  - Backend API:  http://localhost:8000
  - Backend Docs: http://localhost:8000/docs
  - Debug Server: localhost:5678

Para debugging en VS Code:
  1. Ejecutar: python vnm.py up
  2. Abrir VS Code: code .
  3. Presionar F5 -> "Backend: FastAPI Docker Debug"

[FOLDER] Estructura organizada:
  - Script principal: vnm.py (en raiz)
  - Herramientas: devtools/ (organizadas)
  - Documentacion: DEVTOOLS_README.md
""")


def main():
    if len(sys.argv) < 2:
        # Sin argumentos = diagnosticar
        return ejecutar_orquestador(['diagnosticar'])
    
    comando = sys.argv[1].lower()
    
    if comando in ['help', 'h', '--help', '-h']:
        mostrar_ayuda()
        return 0
    elif comando in ['up', 'start', 'iniciar']:
        return ejecutar_orquestador(['iniciar'])
    elif comando in ['down', 'stop', 'terminar']:
        return ejecutar_orquestador(['terminar'])
    elif comando in ['restart', 'reiniciar']:
        print("[RELOAD] Reiniciando entorno...")
        ejecutar_orquestador(['terminar'])
        return ejecutar_orquestador(['iniciar'])
    elif comando in ['clean', 'limpiar']:
        return ejecutar_orquestador(['regenerar'])
    elif comando == 'logs':
        servicio = sys.argv[2] if len(sys.argv) > 2 else None
        return mostrar_logs(servicio)
    elif comando in ['diagnosticar', 'status']:
        return ejecutar_orquestador(['diagnosticar', '--verboso'])
    elif comando == 'backup':
        return ejecutar_orquestador(['backup'])
    elif comando == 'regenerar':
        return ejecutar_orquestador(['regenerar'])
    else:
        print(f"[ERROR] Comando desconocido: {comando}")
        print("[TIP] Usa 'python desarrollo.py help' para ver los comandos disponibles")
        return 1


if __name__ == '__main__':
    sys.exit(main())
