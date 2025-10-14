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
    print(" El servidor iniciará inmediatamente sin esperar debugger.")
    print(" Use WAIT_FOR_CLIENT=true para esperar conexión del debugger.")

    # Verificar si debe esperar el debugger
    wait_for_client = os.environ.get("WAIT_FOR_CLIENT", "false").lower() in (
        "true", "1", "yes", "on"
    )
    
    cmd = [
        "python",
        "-m",
        "debugpy",
        "--listen",
        "0.0.0.0:5678",
    ]
    
    # Solo esperar el debugger si está explícitamente habilitado
    if wait_for_client:
        cmd.append("--wait-for-client")
        print(" Esperando conexión del debugger en puerto 5678...")
    
    cmd.extend([
        "-m",
        "uvicorn",
        "app.main:app",
        "--host",
        "0.0.0.0",
        "--port",
        "8000",
        "--reload",
    ])
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
