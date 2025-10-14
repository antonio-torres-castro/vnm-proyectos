#!/usr/bin/env python3
"""
Script para formatear y verificar el código del proyecto VNM
usando Black y Flake8 con configuración de 79 caracteres.
"""
import subprocess
import sys
from pathlib import Path


def run_command(cmd, description):
    """Ejecutar comando y mostrar resultado"""
    print(f"\n🔧 {description}")
    print(f"   Comando: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        if result.stdout:
            print(f"   ✅ {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"   ❌ Error: {e}")
        if e.stdout:
            print(f"   Stdout: {e.stdout}")
        if e.stderr:
            print(f"   Stderr: {e.stderr}")
        return False


def check_tools():
    """Verificar que las herramientas estén instaladas"""
    print("🔍 Verificando herramientas instaladas...")
    
    # Herramientas obligatorias
    required_tools = [
        (["python", "-m", "black", "--version"], "Black formatter"),
        (["python", "-m", "flake8", "--version"], "Flake8 linter"),
    ]
    
    # Herramientas opcionales
    optional_tools = [
        (["python", "-m", "isort", "--version"], "isort (opcional)"),
    ]
    
    all_ok = True
    for cmd, name in required_tools:
        if not run_command(cmd, f"Verificando {name}"):
            all_ok = False
    
    # Verificar opcionales sin afectar el resultado
    for cmd, name in optional_tools:
        run_command(cmd, f"Verificando {name}")
    
    return all_ok


def format_code():
    """Formatear código con Black"""
    print("\n🎨 Formateando código con Black...")
    
    backend_path = Path("backend")
    if not backend_path.exists():
        print("   ❌ Directorio backend/ no encontrado")
        return False
    
    return run_command(
        ["python", "-m", "black", "--line-length=79", "backend/"],
        "Aplicando Black formatter a backend/"
    )


def check_flake8():
    """Verificar código con Flake8"""
    print("\n🔍 Verificando código con Flake8...")
    
    backend_path = Path("backend")
    if not backend_path.exists():
        print("   ❌ Directorio backend/ no encontrado")
        return False
    
    return run_command(
        ["python", "-m", "flake8", "backend/"],
        "Verificando backend/ con Flake8"
    )


def organize_imports():
    """Organizar imports con isort (si está disponible)"""
    print("\n📦 Organizando imports con isort...")
    
    try:
        subprocess.run(["python", "-m", "isort", "--version"], 
                      capture_output=True, check=True)
        
        return run_command(
            ["python", "-m", "isort", "--profile=black", 
             "--line-length=79", "backend/"],
            "Organizando imports en backend/"
        )
    except subprocess.CalledProcessError:
        print("   ⚠️ isort no está instalado, saltando organización de imports")
        return True


def main():
    """Función principal"""
    print("🚀 FORMATEADOR DE CÓDIGO VNM-PROYECTOS")
    print("=" * 50)
    
    # Verificar herramientas
    if not check_tools():
        print("\n❌ Algunas herramientas no están disponibles")
        print("   Instalar con: pip install black flake8 isort")
        return False
    
    # Ejecutar formateo y verificaciones
    steps = [
        (organize_imports, "Organizar imports"),
        (format_code, "Formatear código"),
        (check_flake8, "Verificar con Flake8"),
    ]
    
    all_success = True
    for step_func, step_name in steps:
        if not step_func():
            print(f"\n❌ Falló: {step_name}")
            all_success = False
        else:
            print(f"   ✅ Completado: {step_name}")
    
    # Resumen final
    print("\n" + "=" * 50)
    if all_success:
        print("🎉 ¡Formateo completado exitosamente!")
        print("   • Código formateado con Black (79 caracteres)")
        print("   • Imports organizados con isort")
        print("   • Verificación Flake8 aprobada")
    else:
        print("⚠️ Formateo completado con algunos errores")
        print("   Revisar los errores mostrados arriba")
    
    return all_success


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
