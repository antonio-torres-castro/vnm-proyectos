#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Instalacion automatica de configuracion VS Code

Autor: MiniMax Agent
"""

import sys
import shutil
from pathlib import Path

def main():
    """Instalar configuracion VS Code"""
    try:
        project_root = Path(__file__).parent.parent
        vscode_dir = project_root / ".vscode"
        backup_dir = project_root / "_vscode"
        
        if backup_dir.exists():
            if vscode_dir.exists():
                shutil.rmtree(vscode_dir)
            shutil.copytree(backup_dir, vscode_dir)
            print("Configuracion VS Code instalada correctamente")
            return 0
        else:
            print("ERROR - No se encontro configuracion de backup")
            return 1
    except Exception as e:
        print(f"ERROR - {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
