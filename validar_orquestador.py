#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Validación del Orquestador
====================================

Verifica que el orquestador esté correctamente configurado y listo para usar.

Autor: MiniMax Agent
"""

import sys
import subprocess
from pathlib import Path


def verificar_python():
    """Verificar versión de Python"""
    print("🐍 Verificando Python...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"   ✓ Python {version.major}.{version.minor}.{version.micro} - OK")
        return True
    else:
        print(f"   ✗ Python {version.major}.{version.minor}.{version.micro} - Requiere Python 3.8+")
        return False


def verificar_docker():
    """Verificar Docker y docker-compose"""
    print("🐳 Verificando Docker...")
    
    try:
        # Verificar docker
        result = subprocess.run(['docker', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"   ✓ {result.stdout.strip()}")
        else:
            print("   ✗ Error ejecutando docker --version")
            return False
        
        # Verificar docker-compose
        result = subprocess.run(['docker-compose', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"   ✓ {result.stdout.strip()}")
        else:
            print("   ✗ Error ejecutando docker-compose --version")
            return False
        
        # Verificar que Docker esté ejecutándose
        result = subprocess.run(['docker', 'info'], capture_output=True, text=True)
        if result.returncode == 0:
            print("   ✓ Docker daemon está ejecutándose")
        else:
            print("   ⚠ Docker daemon no está ejecutándose")
            print("     Ejecuta: sudo systemctl start docker")
            return False
            
        return True
        
    except FileNotFoundError:
        print("   ✗ Docker no está instalado")
        return False
    except PermissionError:
        print("   ✗ Sin permisos para ejecutar Docker")
        print("     Ejecuta: sudo usermod -aG docker $USER")
        print("     Luego reinicia sesión")
        return False


def verificar_archivos():
    """Verificar archivos del proyecto"""
    print("📁 Verificando archivos del proyecto...")
    
    archivos_requeridos = [
        'orquestador_desarrollo.py',
        'desarrollo.py',
        'docker-compose.yml',
        'docker-compose.debug.yml'
    ]
    
    todos_ok = True
    for archivo in archivos_requeridos:
        if Path(archivo).exists():
            print(f"   ✓ {archivo}")
        else:
            print(f"   ✗ {archivo} - No encontrado")
            todos_ok = False
    
    return todos_ok


def verificar_dependencias():
    """Verificar dependencias de Python"""
    print("📦 Verificando dependencias...")
    
    dependencias = ['requests']
    todos_ok = True
    
    for dep in dependencias:
        try:
            __import__(dep)
            print(f"   ✓ {dep}")
        except ImportError:
            print(f"   ✗ {dep} - No instalado")
            print(f"     Ejecuta: pip install {dep}")
            todos_ok = False
    
    return todos_ok


def verificar_estructura():
    """Verificar estructura de directorios"""
    print("🗂️ Verificando estructura de directorios...")
    
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
            print(f"   ✓ {directorio}/")
        else:
            print(f"   ⚠ {directorio}/ - No encontrado")
            if directorio == 'database/backups':
                print("     Se creará automáticamente")
            else:
                todos_ok = False
    
    return todos_ok


def ejecutar_prueba_sintaxis():
    """Verificar sintaxis de los scripts"""
    print("🔍 Verificando sintaxis de scripts...")
    
    scripts = ['orquestador_desarrollo.py', 'desarrollo.py']
    todos_ok = True
    
    for script in scripts:
        try:
            result = subprocess.run([
                sys.executable, '-m', 'py_compile', script
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"   ✓ {script} - Sintaxis OK")
            else:
                print(f"   ✗ {script} - Error de sintaxis")
                print(f"     {result.stderr}")
                todos_ok = False
                
        except Exception as e:
            print(f"   ✗ {script} - Error: {e}")
            todos_ok = False
    
    return todos_ok


def mostrar_comandos_ejemplo():
    """Mostrar comandos de ejemplo"""
    print("\n🚀 Comandos de ejemplo para probar:")
    print("=" * 50)
    print("# Ayuda")
    print("python desarrollo.py help")
    print()
    print("# Diagnóstico")
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
    print("🔧 Validación del Orquestador VNM-Proyectos")
    print("=" * 50)
    
    verificaciones = [
        verificar_python(),
        verificar_docker(),
        verificar_archivos(),
        verificar_dependencias(),
        verificar_estructura(),
        ejecutar_prueba_sintaxis()
    ]
    
    print("\n📊 RESUMEN DE VALIDACIÓN")
    print("=" * 30)
    
    total = len(verificaciones)
    exitosas = sum(verificaciones)
    
    if exitosas == total:
        print("✅ TODAS LAS VERIFICACIONES EXITOSAS")
        print("🎉 El orquestador está listo para usar")
        mostrar_comandos_ejemplo()
        return 0
    else:
        print(f"⚠️ {exitosas}/{total} verificaciones exitosas")
        print("🔧 Corrige los errores antes de usar el orquestador")
        return 1


if __name__ == '__main__':
    sys.exit(main())
