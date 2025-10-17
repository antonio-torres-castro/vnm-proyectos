#!/usr/bin/env python3
"""
Script para revisar los logs de los servicios Docker que estan fallando
"""

import subprocess
import sys
import json
from datetime import datetime

def ejecutar_comando(comando, descripcion=""):
    """Ejecuta un comando y retorna el resultado"""
    print(f"\n{'='*60}")
    print(f"EJECUTANDO: {descripcion}")
    print(f"COMANDO: {comando}")
    print(f"{'='*60}")
    
    try:
        resultado = subprocess.run(
            comando, 
            shell=True, 
            capture_output=True, 
            text=True, 
            encoding='utf-8',
            errors='replace'
        )
        
        if resultado.stdout:
            print("STDOUT:")
            print(resultado.stdout)
        
        if resultado.stderr:
            print("STDERR:")
            print(resultado.stderr)
            
        print(f"EXIT CODE: {resultado.returncode}")
        return resultado
        
    except Exception as e:
        print(f"ERROR ejecutando comando: {e}")
        return None

def main():
    print(f"DIAGNOSTICO DE LOGS - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 1. Logs del backend (ultimas 50 lineas)
    ejecutar_comando(
        "docker logs vnm_backend_debug --tail 50 --timestamps",
        "LOGS DEL BACKEND (ultimas 50 lineas)"
    )
    
    # 2. Logs del frontend (ultimas 50 lineas) 
    ejecutar_comando(
        "docker logs vnm_frontend_debug --tail 50 --timestamps",
        "LOGS DEL FRONTEND (ultimas 50 lineas)"
    )
    
    # 3. Estado detallado de contenedores
    ejecutar_comando(
        "docker ps -a --filter name=vnm_ --format \"table {{.Names}}\\t{{.Status}}\\t{{.Ports}}\"",
        "ESTADO ACTUAL DE CONTENEDORES"
    )
    
    # 4. Inspeccionar healthcheck del backend
    ejecutar_comando(
        "docker inspect vnm_backend_debug --format \"{{json .State.Health}}\"",
        "HEALTHCHECK STATUS DEL BACKEND"
    )

if __name__ == "__main__":
    main()