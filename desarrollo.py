#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Acceso Rápido para Desarrollo VNM-Proyectos
=====================================================

Comandos simplificados para las operaciones más comunes.

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
    return subprocess.run(cmd).returncode


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
        cmd = ['docker-compose', '-f', 'docker-compose.debug.yml', 'logs', '-f']
    
    return subprocess.run(cmd).returncode


def mostrar_ayuda():
    """Mostrar ayuda de comandos"""
    print("""
🚀 Comandos de Desarrollo VNM-Proyectos
========================================

Comandos básicos:
  python desarrollo.py              Diagnosticar estado
  python desarrollo.py up           Iniciar entorno completo
  python desarrollo.py down         Terminar entorno (con backup)
  python desarrollo.py restart      Reiniciar entorno
  python desarrollo.py clean        Limpieza completa + regenerar

Comandos de logs:
  python desarrollo.py logs         Ver todos los logs
  python desarrollo.py logs backend Ver logs del backend
  python desarrollo.py logs postgres Ver logs de PostgreSQL
  
Comandos avanzados:
  python desarrollo.py diagnosticar Diagnóstico detallado
  python desarrollo.py backup       Crear backup manual
  python desarrollo.py regenerar    Regenerar completamente

URLs después de iniciar:
  • Frontend:     http://localhost:3000
  • Backend API:  http://localhost:8000
  • Backend Docs: http://localhost:8000/docs
  • Debug Server: localhost:5678

Para debugging en VS Code:
  1. Ejecutar: python desarrollo.py up
  2. Abrir VS Code: code .
  3. Presionar F5 → "Backend: FastAPI Docker Debug"
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
        print("🔄 Reiniciando entorno...")
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
        print(f"❌ Comando desconocido: {comando}")
        print("💡 Usa 'python desarrollo.py help' para ver los comandos disponibles")
        return 1


if __name__ == '__main__':
    sys.exit(main())
