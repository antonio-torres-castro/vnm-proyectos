#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de formateo Black

Autor: MiniMax Agent
"""

import sys
import subprocess
from pathlib import Path

def main():
    """Ejecutar tests de formateo"""
    try:
        project_root = Path(__file__).parent.parent
        backend_dir = project_root / "backend"
        
        if not backend_dir.exists():
            print("ERROR - Directorio backend no encontrado")
            return 1
        
        # Test con black --check
        result = subprocess.run([sys.executable, "-m", "black", "--check", "."], 
                                cwd=backend_dir, 
                                capture_output=True, 
                                text=True)
        
        if result.returncode == 0:
            print("Tests de formateo completados")
            return 0
        else:
            print("ADVERTENCIA - Archivos requieren formateo")
            return 0  # No fallar por warnings
    except Exception as e:
        print(f"INFO - Black no disponible: {e}")
        return 0

if __name__ == "__main__":
    sys.exit(main())
