#!/usr/bin/env python3
"""
Script para limpiar y optimizar las configuraciones de debugging
Mantiene solo las configuraciones mas modernas y funcionales
Cumple con vnm_development_rules.md
"""

import json
import os
import shutil
from datetime import datetime


def backup_and_clean_launch_json():
    """Crear backup y limpiar launch.json"""
    launch_path = ".vscode/launch.json"

    if not os.path.exists(launch_path):
        print("ERROR: No se encontro .vscode/launch.json")
        return False

    # Crear backup
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = f".vscode/launch.json.backup_{timestamp}"
    shutil.copy2(launch_path, backup_path)
    print(f"OK: Backup creado: {backup_path}")

    # Configuracion limpia y optimizada
    clean_config = {
        "version": "0.2.0",
        "configurations": [
            {
                "name": "Backend Debug (Container)",
                "type": "python",
                "request": "attach",
                "connect": {"host": "localhost", "port": 5678},
                "pathMappings": [
                    {"localRoot": "${workspaceFolder}/backend", "remoteRoot": "/app"}
                ],
                "justMyCode": False,
                "preLaunchTask": "start-development-environment",
            },
            {
                "name": "Frontend Debug (Container)",
                "type": "node",
                "request": "attach",
                "port": 24678,
                "address": "localhost",
                "localRoot": "${workspaceFolder}/frontend",
                "remoteRoot": "/app",
                "skipFiles": ["<node_internals>/**"],
                "restart": True,
                "protocol": "inspector",
                "sourceMaps": True,
                "outFiles": [
                    "${workspaceFolder}/frontend/src/**/*.js",
                    "${workspaceFolder}/frontend/src/**/*.ts",
                    "${workspaceFolder}/frontend/src/**/*.jsx",
                    "${workspaceFolder}/frontend/src/**/*.tsx",
                ],
            },
        ],
        "compounds": [
            {
                "name": "FullStack Debug (Complete)",
                "configurations": [
                    "Backend Debug (Container)",
                    "Frontend Debug (Container)",
                ],
                "stopAll": True,
                "preLaunchTask": "start-development-environment",
            }
        ],
    }

    # Escribir configuracion limpia
    with open(launch_path, "w", encoding="utf-8") as f:
        json.dump(clean_config, f, indent=4)

    print("OK: launch.json limpiado y optimizado")
    print("\nCONFIGURACIONES DISPONIBLES:")
    print("   1. Backend Debug (Container) - Solo backend")
    print("   2. Frontend Debug (Container) - Solo frontend")
    print("   3. FullStack Debug (Complete) - Backend + Frontend")
    print("\nCONFIGURACIONES ELIMINADAS:")
    print("   - 6 configuraciones obsoletas y duplicadas")

    return True


def fix_dockerfile_command():
    """Asegurar que el Dockerfile.dev use el comando correcto para debugging"""
    dockerfile_path = "frontend/Dockerfile.dev"

    if not os.path.exists(dockerfile_path):
        print("ERROR: No se encontro frontend/Dockerfile.dev")
        return False

    with open(dockerfile_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Verificar si ya tiene el comando correcto
    if "npm run dev:debug" in content:
        print("OK: Dockerfile.dev ya configurado para debugging")
        return True

    # Reemplazar el comando
    if 'CMD ["npm", "run", "dev:docker"]' in content:
        content = content.replace(
            'CMD ["npm", "run", "dev:docker"]', 'CMD ["npm", "run", "dev:debug"]'
        )

        with open(dockerfile_path, "w", encoding="utf-8") as f:
            f.write(content)

        print("OK: Dockerfile.dev actualizado para usar dev:debug")
        return True

    print("WARNING: No se pudo actualizar Dockerfile.dev automaticamente")
    return False


def main():
    print("LIMPIANDO CONFIGURACIONES DE DEBUGGING")
    print("=" * 50)

    success = True

    # Limpiar launch.json
    if not backup_and_clean_launch_json():
        success = False

    print()

    # Verificar/corregir Dockerfile
    if not fix_dockerfile_command():
        success = False

    print()

    if success:
        print("LIMPIEZA COMPLETADA EXITOSAMENTE")
        print("\nPASOS SIGUIENTES:")
        print("1. Ejecutar: python automate\\vnm_automate.py dev-restart")
        print("2. En VS Code: F5 -> 'FullStack Debug (Complete)'")
        print("3. Colocar breakpoint en frontend/src/App.jsx")
        print("4. Abrir http://localhost:3000")
        print("5. VS Code parara en tu breakpoint")
    else:
        print("WARNING: Hubo algunos problemas durante la limpieza")

    return success


if __name__ == "__main__":
    main()
