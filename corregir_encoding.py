#!/usr/bin/env python3
"""
Script para corregir problemas de encoding y configuración
que causan fallos en el entorno de desarrollo
"""

import subprocess
import sys
import os
from pathlib import Path

def main():
    print("🔧 CORRECCIÓN DE PROBLEMAS DE ENCODING Y CONFIGURACIÓN")
    print("=" * 60)
    
    # Verificar que estamos en el directorio correcto
    if not Path("docker-compose.debug.yml").exists():
        print("❌ Error: Ejecutar desde el directorio raíz del proyecto")
        sys.exit(1)
    
    print("\n📋 PASOS DE CORRECCIÓN:")
    print("1. ✅ Dockerfile.dev corregido (encoding UTF-8)")
    print("2. ✅ orquestador_desarrollo.py corregido (encoding UTF-8)")
    print("3. 🔄 Limpiando imágenes Docker corruptas...")
    
    # Limpiar imágenes Docker problemáticas
    try:
        # Detener contenedores
        subprocess.run(["docker-compose", "-f", "docker-compose.debug.yml", "down"], 
                      capture_output=True, check=False)
        
        # Eliminar imágenes problemáticas
        subprocess.run(["docker", "image", "rm", "vnm-proyectos-backend"], 
                      capture_output=True, check=False)
        subprocess.run(["docker", "image", "rm", "vnm-proyectos-frontend"], 
                      capture_output=True, check=False)
        
        # Limpiar cache de build
        subprocess.run(["docker", "builder", "prune", "-f"], 
                      capture_output=True, check=False)
        
        print("   ✅ Limpieza de Docker completada")
        
    except Exception as e:
        print(f"   ⚠️  Advertencia en limpieza Docker: {e}")
    
    print("\n4. 🔄 Reconstruyendo entorno...")
    
    # Rebuild con logs verbosos
    try:
        result = subprocess.run([
            "docker-compose", "-f", "docker-compose.debug.yml", 
            "up", "-d", "--build"
        ], capture_output=True, text=True, encoding='utf-8', errors='replace')
        
        if result.returncode == 0:
            print("   ✅ Entorno reconstruido exitosamente")
            print("\n🎯 PRÓXIMOS PASOS:")
            print("   1. Esperar 2-3 minutos para que todos los servicios inicien")
            print("   2. Ejecutar: python automate/vnm_automate.py dev-status")
            print("   3. Si todo está OK, probar debugging con F5 en VS Code")
        else:
            print("   ❌ Error en la reconstrucción:")
            print(f"   STDOUT: {result.stdout}")
            print(f"   STDERR: {result.stderr}")
            
    except Exception as e:
        print(f"   ❌ Error ejecutando docker-compose: {e}")
        print("\n🔧 SOLUCIÓN ALTERNATIVA:")
        print("   Ejecutar manualmente:")
        print("   1. docker-compose -f docker-compose.debug.yml down")
        print("   2. docker-compose -f docker-compose.debug.yml up -d --build")

if __name__ == "__main__":
    main()