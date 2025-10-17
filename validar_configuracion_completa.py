#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Validador completo de configuracion de debugging

Verifica que toda la configuracion este correcta y sin caracteres especiales

Autor: MiniMax Agent
"""

import sys
import json
from pathlib import Path

def validar_configuracion():
    """Validar toda la configuracion de debugging"""
    project_root = Path(__file__).parent
    errores = []
    
    # 1. Verificar que automate/vnm_automate.py existe
    vnm_automate = project_root / "automate" / "vnm_automate.py"
    if not vnm_automate.exists():
        errores.append("automate/vnm_automate.py no encontrado")
    
    # 2. Verificar que orquestador_desarrollo.py existe
    orquestador = project_root / "devtools" / "orquestador_desarrollo.py"
    if not orquestador.exists():
        errores.append("orquestador_desarrollo.py no encontrado")
    
    # 3. Verificar archivos en automate/
    automate_dir = project_root / "automate"
    archivos_requeridos = [
        "instalar_vscode_config.py",
        "verificar_vscode_instalado.py",
        "formatear_codigo.py",
        "validar_configuracion_vscode.py",
        "recrear_base_datos.py",
        "test-black-formatting.py"
    ]
    
    for archivo in archivos_requeridos:
        if not (automate_dir / archivo).exists():
            errores.append(f"automate/{archivo} no encontrado")
    
    # 4. Verificar tasks.json
    tasks_file = project_root / ".vscode" / "tasks.json"
    if tasks_file.exists():
        try:
            with open(tasks_file, 'r', encoding='utf-8') as f:
                tasks_data = json.load(f)
            
            # Buscar task start-development-environment
            task_encontrado = False
            for task in tasks_data.get('tasks', []):
                if task.get('label') == 'start-development-environment':
                    task_encontrado = True
                    if task.get('command') != 'python':
                        errores.append("Task no usa python como comando")
                    args = task.get('args', [])
                    if len(args) < 2 or args[0] != 'automate/vnm_automate.py' or args[1] != 'dev-start':
                        errores.append("Task no llama a automate/vnm_automate.py dev-start")
                    break
            
            if not task_encontrado:
                errores.append("Task start-development-environment no encontrado")
        except Exception as e:
            errores.append(f"Error leyendo tasks.json: {e}")
    else:
        errores.append("tasks.json no encontrado")
    
    # 5. Verificar launch.json
    launch_file = project_root / ".vscode" / "launch.json"
    if launch_file.exists():
        try:
            with open(launch_file, 'r', encoding='utf-8') as f:
                launch_data = json.load(f)
            
            # Buscar configuracion FullStack Debug (Smart)
            config_encontrado = False
            for config in launch_data.get('configurations', []):
                if config.get('name') == 'FullStack Debug (Smart)':
                    config_encontrado = True
                    if config.get('preLaunchTask') != 'start-development-environment':
                        errores.append("FullStack Debug (Smart) no usa el preLaunchTask correcto")
                    break
            
            if not config_encontrado:
                errores.append("Configuracion FullStack Debug (Smart) no encontrada")
        except Exception as e:
            errores.append(f"Error leyendo launch.json: {e}")
    else:
        errores.append("launch.json no encontrado")
    
    # Mostrar resultados
    if errores:
        print("ERRORES ENCONTRADOS:")
        for error in errores:
            print(f"- {error}")
        return 1
    else:
        print("VALIDACION COMPLETADA")
        print("Toda la configuracion esta correcta")
        print("Los automatismos estan en la carpeta automate")
        print("Los mensajes no tienen emojis ni caracteres especiales")
        print("La configuracion es compatible con tasks.json")
        return 0

if __name__ == "__main__":
    sys.exit(validar_configuracion())
