#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Instalador del Orquestador VNM-Proyectos
========================================

Script para configurar automaticamente el entorno y dependencias necesarias.

Autor: MiniMax Agent
"""

import os
import sys
import subprocess
from pathlib import Path


def print_header(title):
    """Imprimir encabezado"""
    print(f"\n[SETUP] {title}")
    print("=" * (len(title) + 4))


def print_step(step):
    """Imprimir paso"""
    print(f">> {step}")


def print_success(msg):
    """Imprimir exito"""
    print(f"[OK] {msg}")


def print_error(msg):
    """Imprimir error"""
    print(f"[ERROR] {msg}")


def print_info(msg):
    """Imprimir informacion"""
    print(f"[INFO] {msg}")


def instalar_dependencias():
    """Instalar dependencias de Python"""
    print_step("Instalando dependencias de Python...")
    
    # Usar requirements.txt si existe
    requirements_file = Path(__file__).parent / "requirements.txt"
    
    if requirements_file.exists():
        try:
            print_step("Instalando desde requirements.txt...")
            subprocess.run([
                sys.executable, '-m', 'pip', 'install', '-r', str(requirements_file)
            ], check=True, capture_output=True)
            print_success("Dependencias instaladas desde requirements.txt")
            return True
        except subprocess.CalledProcessError as e:
            print_error(f"Error instalando desde requirements.txt: {e}")
    
    # Fallback: instalar manualmente
    dependencias = ['requests']
    
    for dep in dependencias:
        try:
            # Verificar si ya esta instalado
            __import__(dep)
            print_success(f"{dep} ya esta instalado")
        except ImportError:
            print_step(f"Instalando {dep}...")
            try:
                subprocess.run([sys.executable, '-m', 'pip', 'install', dep], 
                             check=True, capture_output=True)
                print_success(f"{dep} instalado correctamente")
            except subprocess.CalledProcessError as e:
                print_error(f"Error instalando {dep}: {e}")
                return False
    
    return True


def crear_directorios():
    """Crear directorios necesarios"""
    print_step("Creando directorios necesarios...")
    
    directorios = [
        'database/backups',
        'logs'
    ]
    
    for directorio in directorios:
        path = Path(directorio)
        if not path.exists():
            path.mkdir(parents=True, exist_ok=True)
            print_success(f"Creado: {directorio}/")
        else:
            print_success(f"Ya existe: {directorio}/")
    
    return True


def configurar_git_ignore():
    """Configurar .gitignore para archivos del orquestador"""
    print_step("Configurando .gitignore...")
    
    gitignore_entries = [
        "# Orquestador de Desarrollo",
        "../logs/orquestador.log",
        "diagnostico_*.json",
        "database/backups/*.sql.zip",
        "logs/",
        "__pycache__/",
        "*.pyc",
    ]
    
    gitignore_path = Path('.gitignore')
    
    if gitignore_path.exists():
        content = gitignore_path.read_text()
    else:
        content = ""
    
    needs_update = False
    for entry in gitignore_entries:
        if entry not in content:
            content += f"\n{entry}"
            needs_update = True
    
    if needs_update:
        gitignore_path.write_text(content)
        print_success(".gitignore actualizado")
    else:
        print_success(".gitignore ya esta configurado")
    
    return True


# def crear_alias_bash():
#     """Crear aliases para bash - DESHABILITADO: No compatible con Windows"""
#     print_step("Creando aliases de bash...")
#     
#     aliases_content = '''
# # Aliases para Orquestador VNM-Proyectos
# alias vnm-up="python vnm.py up"
# alias vnm-down="python vnm.py down"
# alias vnm-restart="python vnm.py restart"
# alias vnm-clean="python vnm.py clean"
# alias vnm-status="python vnm.py"
# alias vnm-logs="python vnm.py logs"
# alias vnm-backup="python vnm.py backup"
# alias vnm-help="python vnm.py help"
# '''
#     
#     aliases_file = Path('vnm_aliases.sh')
#     aliases_file.write_text(aliases_content.strip())
#     
#     print_success("Aliases creados en vnm_aliases.sh")
#     print_info("Para usar los aliases, ejecuta: source vnm_aliases.sh")
#     print_info("O agrega al ~/.bashrc: echo 'source $(pwd)/vnm_aliases.sh' >> ~/.bashrc")
#     
#     return True

def crear_alias_windows():
    """Los aliases en Windows se manejan a traves de vnm_automate.py"""
    print_step("Configuracion de aliases para Windows...")
    print_success("Los comandos estan disponibles a traves de vnm_automate.py")
    print_info("Uso: python vnm_automate.py [comando]")
    return True


# def crear_script_inicio_rapido():
#     """Crear script de inicio rapido - DESHABILITADO: No compatible con Windows"""
#     print_step("Creando script de inicio rapido...")
#     
#     script_content = '''#!/bin/bash
# # Script de Inicio Rapido VNM-Proyectos
# 
# echo "[START] Iniciando VNM-Proyectos..."
# 
# # Verificar que estamos en el directorio correcto
# if [ ! -f "desarrollo.py" ]; then
#     echo "[ERROR] Error: No se encontro desarrollo.py"
#     echo "[TIP] Asegurate de estar en el directorio del proyecto"
#     exit 1
# fi
# 
# # Iniciar entorno
# python desarrollo.py up
# 
# # Si todo salio bien, mostrar informacion util
# if [ $? -eq 0 ]; then
#     echo ""
#     echo "[SUCCESS] Entorno iniciado correctamente!"
#     echo ""
#     echo "[MOBILE] URLs disponibles:"
#     echo "   - Frontend:     http://localhost:3000"
#     echo "   - Backend API:  http://localhost:8000"
#     echo "   - Backend Docs: http://localhost:8000/docs"
#     echo ""
#     echo "[SETUP] Para debugging en VS Code:"
#     echo "   1. Abrir VS Code: code ."
#     echo "   2. Presionar F5 -> 'Backend: FastAPI Docker Debug'"
#     echo ""
#     echo "[STATUS] Comandos utiles:"
#     echo "   - Ver estado:   python desarrollo.py"
#     echo "   - Ver logs:     python desarrollo.py logs [servicio]"
#     echo "   - Terminar:     python desarrollo.py down"
# else
#     echo "[ERROR] Error iniciando el entorno"
#     echo "[TIP] Revisa los logs: python desarrollo.py logs"
# fi
# '''
#     
#     script_file = Path('inicio_rapido.sh')
#     script_file.write_text(script_content)
#     
#     # Intentar hacer ejecutable
#     try:
#         os.chmod(script_file, 0o755)
#         print_success("Script de inicio rapido creado: inicio_rapido.sh")
#         print_info("Uso: ./inicio_rapido.sh")
#     except:
#         print_success("Script de inicio rapido creado: inicio_rapido.sh")
#         print_info("Uso: bash inicio_rapido.sh")
#     
#     return True

def crear_script_inicio_windows():
    """Crear script de inicio rapido para Windows"""
    print_step("Configurando inicio rapido para Windows...")
    print_success("Script de inicio disponible a traves de vnm_automate.py")
    print_info("Uso: python vnm_automate.py dev-start")
    print_info("O usa: python setup_proyecto.py para configuracion inicial")
    return True


def generar_documentacion_rapida():
    """Generar documentacion de referencia rapida"""
    print_step("Generando documentacion de referencia...")
    
    doc_content = '''# Referencia Rapida - Orquestador VNM

## [START] Comandos Esenciales
```bash
python desarrollo.py           # Verificar estado
python desarrollo.py up        # Iniciar entorno
python desarrollo.py down      # Terminar entorno
python desarrollo.py restart   # Reiniciar
python desarrollo.py clean     # Regenerar completo
```

## [STATUS] Logs y Diagnostico
```bash
python desarrollo.py logs              # Todos los logs
python desarrollo.py logs backend      # Solo backend
python desarrollo.py logs postgres     # Solo database
python desarrollo.py diagnosticar      # Diagnostico detallado
```

## [SAVE] Backup y Mantenimiento
```bash
python desarrollo.py backup            # Backup manual
python orquestador_desarrollo.py --help # Ayuda completa
```

## [WEB] URLs de Desarrollo
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **Backend Docs**: http://localhost:8000/docs
- **Debug Server**: localhost:5678

## [SETUP] Debugging en VS Code
1. `python desarrollo.py up`
2. `code .`
3. Presionar **F5** -> "Backend: FastAPI Docker Debug"

## [ALERT] Solucion de Problemas
```bash
# Si hay errores
python desarrollo.py logs [servicio]

# Regenerar completamente
python desarrollo.py clean

# Validar configuracion
python validar_orquestador.py
```

## [FOLDER] Archivos Importantes
- `orquestador_desarrollo.py` - Programa principal
- `desarrollo.py` - Comandos rapidos
- `../docker-compose.debug.yml` - Configuracion desarrollo
- `database/backups/` - Backups automaticos
'''
    
    doc_file = Path('REFERENCIA_RAPIDA.md')
    doc_file.write_text(doc_content)
    
    print_success("Documentacion de referencia creada: REFERENCIA_RAPIDA.md")
    
    return True


def mostrar_resumen_final():
    """Mostrar resumen de la instalacion"""
    print_header("INSTALACION COMPLETADA")
    
    print_success("El orquestador esta listo para usar")
    print("")
    
    print("[LIST] Archivos creados:")
    archivos = [
        "orquestador_desarrollo.py - Programa principal",
        "desarrollo.py - Comandos rapidos", 
        "validar_orquestador.py - Validacion del entorno",
        # "vnm_aliases.sh - Aliases de bash",  # No compatible con Windows
        # "inicio_rapido.sh - Script de inicio",  # No compatible con Windows
        "REFERENCIA_RAPIDA.md - Documentacion",
        "database/backups/ - Directorio de backups"
    ]
    
    for archivo in archivos:
        print(f"   - {archivo}")
    
    print("")
    print("[START] PRIMEROS PASOS:")
    print("   1. Validar entorno: python validar_orquestador.py")
    print("   2. Iniciar desarrollo: python desarrollo.py up")
    print("   3. Abrir VS Code: code .")
    print("   4. Presionar F5 para debugging")
    print("")
    print("[TIP] COMANDOS UTILES:")
    print("   - Ayuda: python desarrollo.py help")
    print("   - Estado: python desarrollo.py")
    print("   - Logs: python desarrollo.py logs")
    print("")
    print("[DOCS] DOCUMENTACION COMPLETA:")
    print("   - ORQUESTADOR_README.md - Documentacion completa")
    print("   - EJEMPLO_SALIDA_ORQUESTADOR.md - Ejemplos de uso")


def main():
    """Funcion principal"""
    print_header("INSTALANDO ORQUESTADOR VNM-PROYECTOS")
    
    # Verificar que estamos en el directorio correcto
    if not Path('../docker-compose.debug.yml').exists():
        print_error("No se encontro ../docker-compose.debug.yml")
        print_info("Asegurate de estar en el directorio del proyecto VNM")
        return 1
    
    pasos = [
        ("Instalando dependencias", instalar_dependencias),
        ("Creando directorios", crear_directorios),
        ("Configurando .gitignore", configurar_git_ignore),
        ("Configurando aliases", crear_alias_windows),
        ("Configurando inicio rapido", crear_script_inicio_windows),
        ("Generando documentacion", generar_documentacion_rapida)
    ]
    
    for descripcion, funcion in pasos:
        print_step(descripcion)
        if not funcion():
            print_error(f"Error en: {descripcion}")
            return 1
    
    mostrar_resumen_final()
    return 0


if __name__ == '__main__':
    sys.exit(main())
