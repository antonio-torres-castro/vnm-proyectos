#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para validar que todos los archivos movidos estén en las ubicaciones correctas
y que las referencias en el código estén actualizadas.
"""

import os
import sys
from pathlib import Path

# Configurar encoding para Windows
if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except:
        pass

def print_success(msg):
    print(f"[OK] {msg}")

def print_error(msg):
    print(f"[ERROR] {msg}")

def print_info(msg):
    print(f"[INFO] {msg}")

def validar_estructura_archivos():
    """Validar que todos los archivos estén en las ubicaciones correctas"""
    print("Validando estructura de archivos movidos...\n")
    
    # Cambiar al directorio vnm-proyectos
    os.chdir(Path(__file__).parent.parent)
    
    archivos_esperados = {
        # Archivos que deben estar en vnm-proyectos/
        ".": [
            "docker-compose.yml",
            "docker-compose.debug.yml", 
            "setup.cfg",
            "cspell.json",
            "last_diagnostic.json",
            "instalar_dependencia.txt"
        ],
        # Archivos que deben estar en vnm-proyectos/logs/
        "logs": [
            "orquestador.log"
        ]
    }
    
    archivos_no_deben_existir = [
        # En la raíz del workspace (nivel superior)
        "../docker-compose.yml",
        "../docker-compose.debug.yml",
        "../setup.cfg", 
        "../cspell.json",
        "../last_diagnostic.json",
        "../instalar_dependencia.txt",
        "../orquestador.log",
        "../comandos-desarrollo.sh",
        "../inicio_rapido.sh",
        "../vnm_aliases.sh"
    ]
    
    todos_ok = True
    
    # Verificar archivos que deben existir
    for directorio, archivos in archivos_esperados.items():
        print(f"Verificando directorio: {directorio}/")
        for archivo in archivos:
            ruta = Path(directorio) / archivo if directorio != "." else Path(archivo)
            if ruta.exists():
                print_success(f"   {archivo}")
            else:
                print_error(f"   {archivo} - NO ENCONTRADO")
                todos_ok = False
        print()
    
    # Verificar archivos que NO deben existir
    print("Verificando archivos eliminados/movidos:")
    for archivo in archivos_no_deben_existir:
        if not Path(archivo).exists():
            print_success(f"   {archivo} - Correctamente eliminado/movido")
        else:
            print_error(f"   {archivo} - AÚN EXISTE (debería estar movido)")
            todos_ok = False
    
    print()
    return todos_ok

def validar_referencias_codigo():
    """Validar que las referencias en el código estén actualizadas"""
    print("Validando referencias en el codigo...\n")
    
    archivos_python = list(Path("automate").rglob("*.py"))
    
    referencias_correctas = 0
    referencias_incorrectas = 0
    
    for archivo in archivos_python:
        with open(archivo, 'r', encoding='utf-8') as f:
            contenido = f.read()
        
        # Buscar referencias a docker-compose
        if 'docker-compose.yml' in contenido or 'docker-compose.debug.yml' in contenido:
            # Verificar que tengan ../
            if '../docker-compose' in contenido:
                referencias_correctas += 1
                print_success(f"   {archivo.name} - Referencias docker-compose correctas")
            else:
                referencias_incorrectas += 1
                print_error(f"   {archivo.name} - Referencias docker-compose SIN '../'")
        
        # Buscar referencias a orquestador.log
        if 'orquestador.log' in contenido:
            if '../logs/orquestador.log' in contenido:
                referencias_correctas += 1
                print_success(f"   {archivo.name} - Referencia orquestador.log correcta")
            else:
                referencias_incorrectas += 1
                print_error(f"   {archivo.name} - Referencia orquestador.log incorrecta")
    
    print(f"\nResumen de referencias:")
    print(f"   [OK] Correctas: {referencias_correctas}")
    print(f"   [ERROR] Incorrectas: {referencias_incorrectas}")
    
    return referencias_incorrectas == 0

def main():
    """Función principal"""
    print("VALIDADOR DE ARCHIVOS MOVIDOS")
    print("=" * 50)
    print()
    
    # Validar estructura
    estructura_ok = validar_estructura_archivos()
    
    # Validar referencias
    referencias_ok = validar_referencias_codigo()
    
    print("\n" + "=" * 50)
    if estructura_ok and referencias_ok:
        print_success("VALIDACION COMPLETADA - Todo esta correcto!")
        print_info("Todos los archivos estan en las ubicaciones correctas")
        print_info("Todas las referencias en el codigo estan actualizadas")
    else:
        print_error("VALIDACION FALLIDA - Se encontraron problemas")
        if not estructura_ok:
            print_error("Problemas con la estructura de archivos")
        if not referencias_ok:
            print_error("Problemas con las referencias en el código")
    
    return 0 if (estructura_ok and referencias_ok) else 1

if __name__ == "__main__":
    exit(main())
