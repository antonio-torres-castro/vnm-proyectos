#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fix Subprocess Encoding - Correccion UnicodeDecodeError
========================================================

Script para corregir llamadas subprocess.run() agregando encoding='utf-8'
para prevenir UnicodeDecodeError en Windows.

Archivos objetivo:
- automate/vnm_automate.py
- devtools/orquestador_desarrollo.py

Autor: MiniMax Agent
"""

import os
import re
import shutil
from datetime import datetime
from pathlib import Path


def crear_backup(archivo_path):
    """Crear backup del archivo original"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_path = f"{archivo_path}.backup_{timestamp}"
    shutil.copy2(archivo_path, backup_path)
    print(f"  Backup creado: {backup_path}")
    return backup_path


def corregir_subprocess_calls(contenido):
    """Corregir llamadas subprocess.run() agregando encoding"""
    
    # Patron 1: subprocess.run sin encoding ni errors
    patron1 = r'subprocess\.run\(\s*([^)]+)\s*\)'
    
    def reemplazar_subprocess(match):
        parametros = match.group(1).strip()
        
        # Verificar si ya tiene encoding
        if 'encoding=' in parametros or 'errors=' in parametros:
            return match.group(0)  # No modificar si ya tiene encoding
        
        # Agregar encoding y errors al final
        nuevo = f"subprocess.run(\n                {parametros},\n                encoding='utf-8', errors='replace'\n            )"
        return nuevo
    
    contenido_corregido = re.sub(patron1, reemplazar_subprocess, contenido)
    return contenido_corregido


def procesar_archivo(archivo_path):
    """Procesar un archivo aplicando las correcciones"""
    print(f"\nProcesando: {archivo_path}")
    
    if not os.path.exists(archivo_path):
        print(f"  ERROR: Archivo no encontrado")
        return False
    
    # Crear backup
    backup_path = crear_backup(archivo_path)
    
    try:
        # Leer archivo original
        with open(archivo_path, 'r', encoding='utf-8') as f:
            contenido_original = f.read()
        
        # Aplicar correcciones
        contenido_corregido = corregir_subprocess_calls(contenido_original)
        
        # Verificar si hubo cambios
        if contenido_original == contenido_corregido:
            print("  No se encontraron llamadas subprocess.run() que corregir")
            # Eliminar backup innecesario
            os.remove(backup_path)
            return True
        
        # Escribir archivo corregido
        with open(archivo_path, 'w', encoding='utf-8') as f:
            f.write(contenido_corregido)
        
        # Contar cambios realizados
        cambios = contenido_original.count('subprocess.run(') - contenido_corregido.count('subprocess.run(')
        if cambios < 0:
            cambios = abs(cambios)
        
        print(f"  EXITO: {cambios} llamadas subprocess.run() corregidas")
        
        # Verificar sintaxis Python
        try:
            with open(archivo_path, 'r', encoding='utf-8') as f:
                codigo = f.read()
            compile(codigo, archivo_path, 'exec')
            print("  VALIDACION: Sintaxis Python correcta")
            return True
            
        except SyntaxError as e:
            print(f"  ERROR SINTAXIS: {e}")
            print("  Restaurando archivo original...")
            shutil.copy2(backup_path, archivo_path)
            return False
            
    except Exception as e:
        print(f"  ERROR: {e}")
        if os.path.exists(backup_path):
            print("  Restaurando archivo original...")
            shutil.copy2(backup_path, archivo_path)
        return False


def main():
    """Funcion principal"""
    print("=" * 60)
    print("FIX SUBPROCESS ENCODING - CORRECCION UNICODEDECODEERROR")
    print("=" * 60)
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Archivos a procesar
    archivos = [
        "automate/vnm_automate.py",
        "devtools/orquestador_desarrollo.py"
    ]
    
    print(f"\nArchivos objetivo: {len(archivos)}")
    for archivo in archivos:
        print(f"  - {archivo}")
    
    print("\nIniciando procesamiento...")
    
    exitos = 0
    fallos = 0
    
    for archivo in archivos:
        if procesar_archivo(archivo):
            exitos += 1
        else:
            fallos += 1
    
    print("\n" + "=" * 60)
    print("RESUMEN FINAL")
    print("=" * 60)
    print(f"Archivos procesados: {exitos + fallos}")
    print(f"Exitos: {exitos}")
    print(f"Fallos: {fallos}")
    
    if fallos == 0:
        print("\nCORRECCION COMPLETADA EXITOSAMENTE")
        print("El UnicodeDecodeError debe estar resuelto.")
        print("\nProximos pasos:")
        print("1. Probar: python automate/vnm_automate.py dev-restart")
        print("2. Verificar que no aparezcan errores de encoding")
    else:
        print(f"\nALERTA: {fallos} archivos no pudieron ser corregidos")
        print("Revisar errores arriba y corregir manualmente si es necesario")
    
    return fallos == 0


if __name__ == "__main__":
    exit(0 if main() else 1)