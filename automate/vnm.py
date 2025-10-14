#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VNM - Script de Acceso a Herramientas de Desarrollo
===================================================

Script principal para acceder a las herramientas de desarrollo del proyecto VNM.

Uso:
    python vnm.py [comando]

Comandos disponibles:
    up, down, restart, clean, status, logs, backup, help

Autor: MiniMax Agent
"""

import sys
import subprocess
from pathlib import Path


def main():
    """Función principal que redirige a las herramientas de desarrollo"""
    
    # Ruta a las herramientas de desarrollo
    devtools_path = Path(__file__).parent / "devtools"
    desarrollo_script = devtools_path / "desarrollo.py"
    
    # Verificar que existe el script de desarrollo
    if not desarrollo_script.exists():
        print("❌ Error: No se encontraron las herramientas de desarrollo")
        print("💡 Ejecuta: python devtools/instalar_orquestador.py")
        return 1
    
    # Verificar dependencias básicas
    try:
        import requests  # noqa: F401
    except ImportError:
        print("❌ Error: Falta la dependencia 'requests'")
        print("💡 Ejecuta: pip install requests")
        return 1
    
    # Pasar todos los argumentos al script de desarrollo
    cmd = [sys.executable, str(desarrollo_script)] + sys.argv[1:]
    return subprocess.run(cmd).returncode


if __name__ == '__main__':
    sys.exit(main())
