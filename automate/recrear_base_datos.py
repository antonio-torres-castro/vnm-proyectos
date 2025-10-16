#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Recreador de base de datos

Autor: MiniMax Agent
"""

import sys
import subprocess
from pathlib import Path

def main():
    """Recrear base de datos"""
    try:
        project_root = Path(__file__).parent.parent
        
        # Ejecutar docker-compose down
        result_down = subprocess.run(
            ["docker-compose", "-f", "docker-compose.debug.yml", "down", "-v"],
            cwd=project_root,
            capture_output=True,
            text=True
        )
        
        if result_down.returncode != 0:
            print(f"ADVERTENCIA - Error al detener contenedores: {result_down.stderr}")
        
        # Ejecutar docker-compose up solo postgres
        result_up = subprocess.run(
            ["docker-compose", "-f", "docker-compose.debug.yml", "up", "-d", "postgres"],
            cwd=project_root,
            capture_output=True,
            text=True
        )
        
        if result_up.returncode == 0:
            print("Base de datos recreada correctamente")
            return 0
        else:
            print(f"ERROR - Error al recrear base de datos: {result_up.stderr}")
            return 1
    except Exception as e:
        print(f"ERROR - {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
