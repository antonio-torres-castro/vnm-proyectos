#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Formateador de codigo Python

Autor: MiniMax Agent
"""

import sys
import subprocess
from pathlib import Path

def main():
    """Formatear codigo Python"""
    try:
        project_root = Path(__file__).parent.parent
        backend_dir = project_root / "backend"
        
        if not backend_dir.exists():
            print("ERROR - Directorio backend no encontrado")
            return 1
        
        # Formatear con black
        result = subprocess.run([sys.executable, "-m", "black", "."], 
                                cwd=backend_dir, 
                                capture_output=True, 
                                text=True)
        
        if result.returncode == 0:
            print("Codigo formateado correctamente")
            return 0
        else:
            print(f"ERROR - Error al formatear: {result.stderr}")
            return 1
    except Exception as e:
        print(f"ERROR - {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
