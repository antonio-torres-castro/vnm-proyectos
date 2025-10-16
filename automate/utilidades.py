#!/usr/bin/env python3
"""
Utilidades simplificadas para el proyecto vnm-proyectos
"""
import subprocess
import sys
import os
import platform
from pathlib import Path

def ejecutar_comando(comando, mostrar_salida=True, capturar_salida=False, directorio=None):
    """
    Ejecuta un comando del sistema
    
    Args:
        comando: Comando a ejecutar
        mostrar_salida: Si mostrar la salida en tiempo real
        capturar_salida: Si capturar la salida para retornar
        directorio: Directorio donde ejecutar el comando
    
    Returns:
        tuple: (exito, salida, error)
    """
    try:
        if capturar_salida:
            resultado = subprocess.run(
                comando, 
                shell=True, 
                capture_output=True, 
                text=True,
                cwd=directorio,
                check=True
            )
            return True, resultado.stdout, resultado.stderr
        else:
            resultado = subprocess.run(
                comando, 
                shell=True,
                cwd=directorio,
                check=True
            )
            return True, "", ""
    except subprocess.CalledProcessError as e:
        error_msg = f"Error ejecutando: {comando}\nCodigo: {e.returncode}"
        if hasattr(e, 'stderr') and e.stderr:
            error_msg += f"\nError: {e.stderr}"
        return False, "", error_msg
    except Exception as e:
        return False, "", str(e)

def verificar_archivo_existe(ruta_archivo):
    """Verifica si un archivo existe"""
    return Path(ruta_archivo).exists()

def verificar_directorio_existe(ruta_directorio):
    """Verifica si un directorio existe"""
    return Path(ruta_directorio).is_dir()

def obtener_raiz_proyecto():
    """Obtiene la ruta raiz del proyecto"""
    return Path(__file__).parent.parent.absolute()

def verificar_python():
    """Verifica la instalacion de Python"""
    try:
        version = sys.version_info
        if version.major >= 3 and version.minor >= 8:
            return True, f"Python {version.major}.{version.minor}.{version.micro}"
        else:
            return False, f"Python {version.major}.{version.minor}.{version.micro} (se requiere 3.8+)"
    except Exception as e:
        return False, f"Error verificando Python: {e}"

def verificar_node():
    """Verifica la instalacion de Node.js"""
    exito, salida, error = ejecutar_comando("node --version", capturar_salida=True, mostrar_salida=False)
    if exito:
        return True, f"Node.js {salida.strip()}"
    else:
        return False, "Node.js no encontrado"

def verificar_npm():
    """Verifica la instalacion de npm"""
    exito, salida, error = ejecutar_comando("npm --version", capturar_salida=True, mostrar_salida=False)
    if exito:
        return True, f"npm {salida.strip()}"
    else:
        return False, "npm no encontrado"

def verificar_docker():
    """Verifica la instalacion de Docker"""
    exito, salida, error = ejecutar_comando("docker --version", capturar_salida=True, mostrar_salida=False)
    if exito:
        return True, f"Docker {salida.strip()}"
    else:
        return False, "Docker no encontrado"

def verificar_vscode():
    """Verifica la instalacion de VS Code"""
    exito, salida, error = ejecutar_comando("code --version", capturar_salida=True, mostrar_salida=False)
    if exito:
        version = salida.strip().split('\n')[0]
        return True, f"VS Code {version}"
    else:
        return False, "VS Code no encontrado"

def verificar_ambiente_virtual():
    """Verifica si hay un ambiente virtual activo"""
    raiz = obtener_raiz_proyecto()
    venv_path = raiz / ".venv"
    
    if venv_path.exists():
        if platform.system() == "Windows":
            python_exe = venv_path / "Scripts" / "python.exe"
        else:
            python_exe = venv_path / "bin" / "python"
        
        if python_exe.exists():
            return True, f"Ambiente virtual encontrado en: {venv_path}"
        else:
            return False, f"Directorio .venv existe pero no tiene Python ejecutable"
    else:
        return False, "No se encontro ambiente virtual en .venv"

def diagnostico_completo():
    """Ejecuta un diagnostico completo del sistema"""
    print("DIAGNOSTICO DEL SISTEMA")
    print("=" * 50)
    
    verificaciones = [
        ("Python", verificar_python),
        ("Node.js", verificar_node),
        ("npm", verificar_npm),
        ("Docker", verificar_docker),
        ("VS Code", verificar_vscode),
        ("Ambiente Virtual", verificar_ambiente_virtual)
    ]
    
    resultados = {}
    
    for nombre, funcion in verificaciones:
        exito, mensaje = funcion()
        resultados[nombre] = (exito, mensaje)
        
        status = "✓" if exito else "✗"
        print(f"{status} {nombre}: {mensaje}")
    
    print("\n" + "=" * 50)
    exitosos = sum(1 for exito, _ in resultados.values() if exito)
    total = len(resultados)
    print(f"RESUMEN: {exitosos}/{total} verificaciones exitosas")
    
    if exitosos == total:
        print("✓ Sistema listo para desarrollo")
    else:
        print("⚠ Hay problemas que resolver antes de continuar")
    
    return resultados

def main():
    """Funcion principal para uso como script independiente"""
    if len(sys.argv) > 1:
        if sys.argv[1] == "--diagnostico" or sys.argv[1] == "-d":
            diagnostico_completo()
        elif sys.argv[1] == "--help" or sys.argv[1] == "-h":
            print("Utilidades para vnm-proyectos")
            print("Uso: python utilidades.py [opcion]")
            print("\nOpciones:")
            print("  -d, --diagnostico    Ejecutar diagnostico completo")
            print("  -h, --help          Mostrar esta ayuda")
        else:
            print(f"Opcion desconocida: {sys.argv[1]}")
            print("Usa --help para ver opciones disponibles")
    else:
        print("Utilidades para vnm-proyectos")
        print("Usa --help para ver opciones disponibles")

if __name__ == "__main__":
    main()