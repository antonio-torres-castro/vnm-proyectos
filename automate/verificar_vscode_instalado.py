#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verificacion de configuracion VS Code

Autor: MiniMax Agent
"""

import sys
from pathlib import Path

def main():
    """Verificar configuracion VS Code"""
    try:
        project_root = Path(__file__).parent.parent
        vscode_dir = project_root / ".vscode"
        required_files = ['launch.json', 'tasks.json', 'settings.json']
        
        missing_files = []
        for file in required_files:
            if not (vscode_dir / file).exists():
                missing_files.append(file)
        
        if missing_files:
            print(f"ERROR - Archivos faltantes: {', '.join(missing_files)}")
            return 1
        
        print("Configuracion VS Code verificada correctamente")
        return 0
    except Exception as e:
        print(f"ERROR - {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
