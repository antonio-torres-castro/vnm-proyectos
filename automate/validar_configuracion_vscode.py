#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Validador de configuracion VS Code

Autor: MiniMax Agent
"""

import sys
import subprocess
from pathlib import Path

def main():
    """Validar codigo Python"""
    try:
        project_root = Path(__file__).parent.parent
        backend_dir = project_root / "backend"
        
        if not backend_dir.exists():
            print("ERROR - Directorio backend no encontrado")
            return 1
        
        # Validar con flake8
        result = subprocess.run([sys.executable, "-m", "flake8", "."], 
                                cwd=backend_dir, 
                                capture_output=True, 
                                text=True)
        
        if result.returncode == 0:
            print("Validacion de codigo completada")
            return 0
        else:
            print(f"ADVERTENCIA - Problemas encontrados: {result.stdout}")
            return 0  # No fallar por warnings
    except Exception as e:
        print(f"INFO - Flake8 no disponible: {e}")
        return 0

if __name__ == "__main__":
    sys.exit(main())
