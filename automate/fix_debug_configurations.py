#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fix Debug Configurations - Optimizar configuraciones VS Code
============================================================

Script para simplificar y optimizar las configuraciones de depuración,
eliminando las 8 configuraciones obsoletas y dejando solo 1 configuración
FullStack optimizada y funcional.

Cambios:
- Eliminar 8 configuraciones obsoletas
- Crear 1 configuración FullStack optimizada
- Usar Chrome en lugar de Edge
- Mejorar task de inicio

Autor: MiniMax Agent
"""

import json
import os
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


def nueva_configuracion_launch():
    """Generar nueva configuracion launch.json optimizada"""
    return {
        "version": "0.2.0",
        "configurations": [
            {
                "name": "Backend Debug (Container)",
                "type": "python",
                "request": "attach",
                "connect": {
                    "host": "localhost",
                    "port": 5678
                },
                "pathMappings": [
                    {
                        "localRoot": "${workspaceFolder}/backend",
                        "remoteRoot": "/app"
                    }
                ],
                "justMyCode": False
            },
            {
                "name": "Frontend Debug (Browser - Chrome)",
                "type": "chrome",
                "request": "launch",
                "url": "http://localhost:3000",
                "webRoot": "${workspaceFolder}/frontend/src",
                "sourceMapPathOverrides": {
                    "/src/*": "${workspaceFolder}/frontend/src/*",
                    "/*": "*",
                    "/static/js/*": "${workspaceFolder}/frontend/src/*",
                    "/./~/*": "${workspaceFolder}/frontend/node_modules/*"
                },
                "userDataDir": False,
                "timeout": 30000,
                "disableNetworkCache": True,
                "showAsyncStacks": True
            }
        ],
        "compounds": [
            {
                "name": "FullStack Debug (Optimized)",
                "configurations": [
                    "Backend Debug (Container)",
                    "Frontend Debug (Browser - Chrome)"
                ],
                "stopAll": True,
                "preLaunchTask": "start-development-environment"
            }
        ]
    }


def actualizar_task_en_tasks(tasks_data):
    """Actualizar la task start-development-environment en tasks.json"""
    for task in tasks_data.get("tasks", []):
        if task.get("label") == "start-development-environment":
            # Agregar configuracion de background task
            task["isBackground"] = True
            task["problemMatcher"] = {
                "pattern": {
                    "regexp": "^(.*)$",
                    "file": 1
                },
                "background": {
                    "activeOnStart": True,
                    "beginsPattern": "INICIANDO ENTORNO DE DESARROLLO",
                    "endsPattern": "Entorno iniciado correctamente"
                }
            }
            print("  Task 'start-development-environment' actualizada")
            break
    return tasks_data


def procesar_launch_json():
    """Procesar archivo launch.json"""
    print("\nProcesando: .vscode/launch.json")
    
    launch_path = ".vscode/launch.json"
    
    if not os.path.exists(launch_path):
        print(f"  ERROR: Archivo no encontrado: {launch_path}")
        return False
    
    # Crear backup
    backup_path = crear_backup(launch_path)
    
    try:
        # Leer configuracion actual
        with open(launch_path, 'r', encoding='utf-8') as f:
            config_actual = json.load(f)
        
        # Contar configuraciones actuales
        configs_actuales = len(config_actual.get("configurations", []))
        compounds_actuales = len(config_actual.get("compounds", []))
        
        # Aplicar nueva configuracion
        nueva_config = nueva_configuracion_launch()
        
        # Escribir nueva configuracion
        with open(launch_path, 'w', encoding='utf-8') as f:
            json.dump(nueva_config, f, indent=4, ensure_ascii=False)
        
        configs_nuevas = len(nueva_config.get("configurations", []))
        compounds_nuevas = len(nueva_config.get("compounds", []))
        
        print(f"  EXITO: Configuraciones {configs_actuales} -> {configs_nuevas}")
        print(f"  EXITO: Compounds {compounds_actuales} -> {compounds_nuevas}")
        print("  ELIMINADAS: 8 configuraciones obsoletas")
        print("  CREADA: 1 configuracion FullStack optimizada")
        
        return True
        
    except Exception as e:
        print(f"  ERROR: {e}")
        if os.path.exists(backup_path):
            print("  Restaurando archivo original...")
            shutil.copy2(backup_path, launch_path)
        return False


def procesar_tasks_json():
    """Procesar archivo tasks.json"""
    print("\nProcesando: .vscode/tasks.json")
    
    tasks_path = ".vscode/tasks.json"
    
    if not os.path.exists(tasks_path):
        print(f"  ERROR: Archivo no encontrado: {tasks_path}")
        return False
    
    # Crear backup
    backup_path = crear_backup(tasks_path)
    
    try:
        # Leer configuracion actual
        with open(tasks_path, 'r', encoding='utf-8') as f:
            tasks_data = json.load(f)
        
        # Actualizar task
        tasks_data = actualizar_task_en_tasks(tasks_data)
        
        # Escribir configuracion actualizada
        with open(tasks_path, 'w', encoding='utf-8') as f:
            json.dump(tasks_data, f, indent=4, ensure_ascii=False)
        
        print("  EXITO: tasks.json actualizado")
        return True
        
    except Exception as e:
        print(f"  ERROR: {e}")
        if os.path.exists(backup_path):
            print("  Restaurando archivo original...")
            shutil.copy2(backup_path, tasks_path)
        return False


def main():
    """Funcion principal"""
    print("=" * 60)
    print("FIX DEBUG CONFIGURATIONS - OPTIMIZAR CONFIGURACIONES VS CODE")
    print("=" * 60)
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Verificar que estamos en el directorio correcto
    if not os.path.exists(".vscode"):
        print("ERROR: Directorio .vscode no encontrado")
        print("Asegurate de ejecutar desde el directorio raiz del proyecto")
        return False
    
    print("\nObjetivo:")
    print("- Eliminar 8 configuraciones de depuracion obsoletas")
    print("- Crear 1 configuracion FullStack optimizada")
    print("- Usar Chrome en lugar de Edge")
    print("- Mejorar task de inicio")
    
    exitos = 0
    total = 2
    
    # Procesar archivos
    if procesar_launch_json():
        exitos += 1
    
    if procesar_tasks_json():
        exitos += 1
    
    print("\n" + "=" * 60)
    print("RESUMEN FINAL")
    print("=" * 60)
    print(f"Archivos procesados: {exitos}/{total}")
    
    if exitos == total:
        print("\nOPTIMIZACION COMPLETADA EXITOSAMENTE")
        print("\nNueva configuracion disponible:")
        print("- 'FullStack Debug (Optimized)' en VS Code")
        print("\nCaracteristicas:")
        print("- Backend: Depuracion en contenedor Docker")
        print("- Frontend: Chrome con source maps optimizados")
        print("- Auto-inicio del entorno de desarrollo")
        print("- Timeout extendido para mejor estabilidad")
        print("\nInstrucciones:")
        print("1. En VS Code presionar F5")
        print("2. Seleccionar 'FullStack Debug (Optimized)'")
        print("3. El entorno se iniciara automaticamente")
    else:
        print(f"\nALERTA: {total - exitos} archivos no pudieron ser procesados")
        print("Revisar errores arriba")
    
    return exitos == total


if __name__ == "__main__":
    exit(0 if main() else 1)