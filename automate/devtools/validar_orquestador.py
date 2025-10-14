#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Validacion del Orquestador
====================================

Verifica que el orquestador este correctamente configurado y listo para usar.

Autor: MiniMax Agent
"""

import sys
import subprocess
from pathlib import Path


def verificar_python():
    """Verificar version de Python"""
    print("[PYTHON] Verificando Python...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"   [OK] Python {version.major}.{version.minor}.{version.micro} - OK")
        return True
    else:
        print(f"   [ERROR] Python {version.major}.{version.minor}.{version.micro} - Requiere Python 3.8+")
        return False


def verificar_docker():
    """Verificar Docker y docker-compose"""
    print("[DOCKER] Verificando Docker...")
    
    try:
        # Verificar docker
        result = subprocess.run(['docker', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"   [OK] {result.stdout.strip()}")
        else:
            print("   [ERROR] Error ejecutando docker --version")
            return False
        
        # Verificar docker-compose
        result = subprocess.run(['docker-compose', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"   [OK] {result.stdout.strip()}")
        else:
            print("   [ERROR] Error ejecutando docker-compose --version")
            return False
        
        # Verificar que Docker este ejecutandose
        result = subprocess.run(['docker', 'info'], capture_output=True, text=True)
        if result.returncode == 0:
            print("   [OK] Docker daemon esta ejecutandose")
        else:
            print("   [WARN] Docker daemon no esta ejecutandose")
            print("     Ejecuta: sudo systemctl start docker")
            return False
            
        return True
        
    except FileNotFoundError:
        print("   [ERROR] Docker no esta instalado")
        return False
    except PermissionError:
        print("   [ERROR] Sin permisos para ejecutar Docker")
        print("     Ejecuta: sudo usermod -aG docker $USER")
        print("     Luego reinicia sesion")
        return False


def verificar_archivos():
    """Verificar archivos del proyecto"""
    print("[FOLDER] Verificando archivos del proyecto...")
    
    archivos_requeridos = [
        'orquestador_desarrollo.py',
        'desarrollo.py',
        '../docker-compose.yml',
        '../docker-compose.debug.yml'
    ]
    
    todos_ok = True
    for archivo in archivos_requeridos:
        if Path(archivo).exists():
            print(f"   [OK] {archivo}")
        else:
            print(f"   [ERROR] {archivo} - No encontrado")
            todos_ok = False
    
    return todos_ok


def verificar_dependencias():
    """Verificar dependencias de Python"""
    print("[PKG] Verificando dependencias...")
    
    dependencias = ['requests']
    todos_ok = True
    
    for dep in dependencias:
        try:
            __import__(dep)
            print(f"   [OK] {dep}")
        except ImportError:
            print(f"   [ERROR] {dep} - No instalado")
            print(f"     Ejecuta: pip install {dep}")
            todos_ok = False
    
    return todos_ok


def verificar_estructura():
    """Verificar estructura de directorios"""
    print("[FOLDER] Verificando estructura de directorios...")
    
    directorios = [
        'backend',
        'frontend', 
        'database',
        'database/init-data',
        'database/backups'
    ]
    
    todos_ok = True
    for directorio in directorios:
        path = Path(directorio)
        if path.exists():
            print(f"   [OK] {directorio}/")
        else:
            print(f"   [WARN] {directorio}/ - No encontrado")
            if directorio == 'database/backups':
                print("     Se creara automaticamente")
            else:
                todos_ok = False
    
    return todos_ok


def ejecutar_prueba_sintaxis():
    """Verificar sintaxis de los scripts"""
    print("[SEARCH] Verificando sintaxis de scripts...")
    
    scripts = ['orquestador_desarrollo.py', 'desarrollo.py']
    todos_ok = True
    
    for script in scripts:
        try:
            result = subprocess.run([
                sys.executable, '-m', 'py_compile', script
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"   [OK] {script} - Sintaxis OK")
            else:
                print(f"   [ERROR] {script} - Error de sintaxis")
                print(f"     {result.stderr}")
                todos_ok = False
                
        except Exception as e:
            print(f"   [ERROR] {script} - Error: {e}")
            todos_ok = False
    
    return todos_ok


def mostrar_comandos_ejemplo():
    """Mostrar comandos de ejemplo"""
    print("\n[START] Comandos de ejemplo para probar:")
    print("=" * 50)
    print("# Ayuda")
    print("python desarrollo.py help")
    print()
    print("# Diagnostico")
    print("python desarrollo.py")
    print()
    print("# Iniciar entorno")
    print("python desarrollo.py up")
    print()
    print("# Ver logs")
    print("python desarrollo.py logs")
    print()
    print("# Terminar entorno")
    print("python desarrollo.py down")


def main():
    print("[SETUP] Validacion del Orquestador VNM-Proyectos")
    print("=" * 50)
    
    verificaciones = [
        verificar_python(),
        verificar_docker(),
        verificar_archivos(),
        verificar_dependencias(),
        verificar_estructura(),
        ejecutar_prueba_sintaxis()
    ]
    
    print("\n[STATUS] RESUMEN DE VALIDACION")
    print("=" * 30)
    
    total = len(verificaciones)
    exitosas = sum(verificaciones)
    
    if exitosas == total:
        print("[OK] TODAS LAS VERIFICACIONES EXITOSAS")
        print("[SUCCESS] El orquestador esta listo para usar")
        mostrar_comandos_ejemplo()
        return 0
    else:
        print(f"[WARN] {exitosas}/{total} verificaciones exitosas")
        print("[SETUP] Corrige los errores antes de usar el orquestador")
        return 1


if __name__ == '__main__':
    sys.exit(main())
