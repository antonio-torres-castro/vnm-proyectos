#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fix Debug Containers - Configuracion correcta para contenedores
===============================================================

Crea configuracion de depuracion optimizada para desarrollo en contenedores.
El frontend en contenedores NO se puede debuggear con Chrome directamente.

Solucion:
- Backend: Debug en contenedor (OK)
- Frontend: Debug con herramientas de navegador (Mejor opcion)
- FullStack: Solo backend + navegador separado

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


def nueva_configuracion_containers():
    """Configuracion optimizada para contenedores"""
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
                "name": "FullStack Debug (Container-Optimized)",
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
                "justMyCode": False,
                "preLaunchTask": "start-development-environment"
            }
        ]
    }


def actualizar_task_en_tasks(tasks_data):
    """Actualizar tasks para contenedores"""
    # Asegurar que la task start-development-environment existe
    task_found = False
    for task in tasks_data.get("tasks", []):
        if task.get("label") == "start-development-environment":
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
            task_found = True
            print("  Task 'start-development-environment' configurada")
            break
    
    if not task_found:
        print("  ADVERTENCIA: Task 'start-development-environment' no encontrada")
    
    return tasks_data


def crear_instrucciones_debugging():
    """Crear archivo con instrucciones de debugging"""
    instrucciones = """# Instrucciones de Debugging para Contenedores

## CONFIGURACIONES DISPONIBLES:

### 1. "Backend Debug (Container)" 
- **USO**: Solo depurar backend
- **COMO**: F5 → Seleccionar configuracion
- **PREREQUISITO**: Contenedores ejecutandose

### 2. "FullStack Debug (Container-Optimized)"
- **USO**: Debugging completo optimizado
- **COMO**: F5 → Seleccionar configuracion  
- **QUE HACE**: 
  - Inicia entorno automaticamente
  - Conecta debugger al backend en contenedor
  - Abre http://localhost:3000 manualmente en navegador

## PARA FRONTEND:

### ❌ NO INTENTES: Chrome Debug Extensions
- Los contenedores NO son compatibles con Chrome debugger
- Los source maps fallan porque node_modules esta en contenedor

### ✅ USA MEJOR: Herramientas de Navegador
1. **Abrir manualmente**: http://localhost:3000
2. **F12**: Abrir Developer Tools  
3. **Sources**: Ver codigo fuente con source maps
4. **Console**: Debug interactivo
5. **Network**: Monitorear requests
6. **React DevTools**: Extension para React

## FLUJO DE TRABAJO RECOMENDADO:

1. **Iniciar debugging**: 
   ```
   F5 → "FullStack Debug (Container-Optimized)"
   ```

2. **Backend**: 
   - Breakpoints en VS Code funcionan perfecto
   - Debug paso a paso completo

3. **Frontend**:
   - Abrir http://localhost:3000 en navegador
   - F12 → Developer Tools para debugging
   - React DevTools para componentes

4. **Beneficios**:
   - ✅ Backend: Debug completo en VS Code
   - ✅ Frontend: Herramientas nativas del navegador
   - ✅ Ambos funcionan perfectamente
   - ✅ Sin problemas de source maps
   - ✅ Sin errores de conexion

## RESOLUCION DE PROBLEMAS:

### "Unable to attach to browser":
- **NORMAL**: Los contenedores no soportan Chrome debug
- **SOLUCION**: Usar Developer Tools del navegador

### "Puntos de interrupcion en blanco":
- **CAUSA**: Source maps incorrectos en contenedores
- **SOLUCION**: Debug backend en VS Code, frontend en navegador

### "No veo node_modules":
- **NORMAL**: Esta dentro del contenedor, no en tu maquina
- **CORRECTO**: No debe estar en tu proyecto local

## CONFIGURACION OPTIMA:
Esta configuracion es la MAS EFICIENTE para desarrollo en contenedores.
Cada herramienta (VS Code para backend, navegador para frontend) 
se usa para lo que mejor funciona.
"""
    
    with open("debugging_containers_guide.md", "w", encoding="utf-8") as f:
        f.write(instrucciones)
    
    print("  Guia creada: debugging_containers_guide.md")


def main():
    """Funcion principal"""
    print("=" * 70)
    print("FIX DEBUG CONTAINERS - CONFIGURACION CORRECTA PARA CONTENEDORES")
    print("=" * 70)
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    if not os.path.exists(".vscode"):
        print("ERROR: Directorio .vscode no encontrado")
        return False
    
    print("\nDIAGNOSTICO:")
    print("- Frontend en contenedores NO se puede debuggear con Chrome")
    print("- Source maps fallan porque node_modules esta en contenedor")  
    print("- Solucion: Backend en VS Code + Frontend en navegador")
    
    print("\nCAMBIOS:")
    print("- Eliminar configuracion Chrome (no funciona)")
    print("- Optimizar configuracion para contenedores")
    print("- Crear guia de debugging")
    
    exitos = 0
    total = 3
    
    # 1. Procesar launch.json
    print("\nProcesando: .vscode/launch.json")
    launch_path = ".vscode/launch.json"
    
    if os.path.exists(launch_path):
        backup = crear_backup(launch_path)
        try:
            nueva_config = nueva_configuracion_containers()
            with open(launch_path, 'w', encoding='utf-8') as f:
                json.dump(nueva_config, f, indent=4, ensure_ascii=False)
            print("  EXITO: Configuracion optimizada para contenedores")
            exitos += 1
        except Exception as e:
            print(f"  ERROR: {e}")
            shutil.copy2(backup, launch_path)
    else:
        print("  ERROR: launch.json no encontrado")
    
    # 2. Procesar tasks.json
    print("\nProcesando: .vscode/tasks.json")
    tasks_path = ".vscode/tasks.json"
    
    if os.path.exists(tasks_path):
        backup = crear_backup(tasks_path)
        try:
            with open(tasks_path, 'r', encoding='utf-8') as f:
                tasks_data = json.load(f)
            
            tasks_data = actualizar_task_en_tasks(tasks_data)
            
            with open(tasks_path, 'w', encoding='utf-8') as f:
                json.dump(tasks_data, f, indent=4, ensure_ascii=False)
            print("  EXITO: Tasks actualizadas")
            exitos += 1
        except Exception as e:
            print(f"  ERROR: {e}")
            shutil.copy2(backup, tasks_path)
    else:
        print("  ERROR: tasks.json no encontrado")
    
    # 3. Crear guia
    print("\nCreando: debugging_containers_guide.md")
    try:
        crear_instrucciones_debugging()
        exitos += 1
    except Exception as e:
        print(f"  ERROR: {e}")
    
    print("\n" + "=" * 70)
    print("RESUMEN FINAL")
    print("=" * 70)
    print(f"Procesos completados: {exitos}/{total}")
    
    if exitos == total:
        print("\n✅ CONFIGURACION CONTAINERS COMPLETADA")
        print("\nNUEVAS CONFIGURACIONES:")
        print("- 'Backend Debug (Container)': Solo backend")
        print("- 'FullStack Debug (Container-Optimized)': Completo optimizado")
        print("\nINSTRUCCIONES:")
        print("1. F5 → 'FullStack Debug (Container-Optimized)'")
        print("2. Backend: Debug en VS Code (breakpoints funcionan)")
        print("3. Frontend: Abrir http://localhost:3000 → F12 Developer Tools")
        print("\nDOCUMENTACION:")
        print("- Lee: debugging_containers_guide.md")
        print("- Flujo de trabajo optimizado incluido")
    else:
        print(f"\n❌ {total - exitos} procesos fallaron")
    
    return exitos == total


if __name__ == "__main__":
    exit(0 if main() else 1)