#!/usr/bin/env python3
"""
Script de inicio para el backend con soporte de debugging opcional
"""
import os
import subprocess
import sys

# typing imports removidos - no utilizados


def run_with_debug():
    """Ejecutar con debugpy (debugging remoto)"""
    print(" Iniciando servidor con debugging habilitado...")
    print(" Debug server listening on 0.0.0.0:5678")
    print(
        (
            " Para conectar desde VS Code, usa la configuración "
            "'Python: FastAPI Docker Attach'"
        )
    )

    cmd = [
        "python",
        "-m",
        "debugpy",
        "--listen",
        "0.0.0.0:5678",
        "--wait-for-client",
        "-m",
        "uvicorn",
        "app.main:app",
        "--host",
        "0.0.0.0",
        "--port",
        "8000",
        "--reload",
    ]
    subprocess.run(cmd)


def run_normal():
    """Ejecutar sin debugging"""
    print(" Iniciando servidor sin debugging...")

    cmd = [
        "uvicorn",
        "app.main:app",
        "--host",
        "0.0.0.0",
        "--port",
        "8000",
        "--reload",
    ]
    subprocess.run(cmd)


if __name__ == "__main__":
    debug_mode = os.environ.get("ENABLE_DEBUG", "false").lower() in (
        "true",
        "1",
        "yes",
        "on",
    )

    if len(sys.argv) > 1:
        if sys.argv[1] == "--debug":
            debug_mode = True
        elif sys.argv[1] == "--no-debug":
            debug_mode = False

    if debug_mode:
        run_with_debug()
    else:
        run_normal()
