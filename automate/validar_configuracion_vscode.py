#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Validador de Configuración VS Code - FullStack Debug
Verifica que la configuración de debugging esté correcta
"""

import json
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

def validar_configuracion():
    """Valida la configuración de VS Code para debugging"""
    
    print("Validando configuracion de VS Code...")
    
    errores = []
    warnings = []
    
    # Verificar que existe la carpeta .vscode en vnm-proyectos
    vscode_dir = Path("../.vscode")
    if not vscode_dir.exists():
        errores.append("[ERROR] Carpeta .vscode no existe en vnm-proyectos/")
        return errores, warnings
    
    # Verificar launch.json
    launch_file = vscode_dir / "launch.json"
    if not launch_file.exists():
        errores.append("[ERROR] Archivo .vscode/launch.json no existe")
    else:
        try:
            with open(launch_file, 'r', encoding='utf-8') as f:
                launch_config = json.load(f)
            
            # Verificar configuraciones
            configs = launch_config.get('configurations', [])
            config_names = [c.get('name') for c in configs]
            
            # Verificar que existan las configuraciones necesarias
            required_configs = [
                "Frontend Debug",
                "Backend Debug", 
                "FullStack Debug - Ambos simultáneamente"
            ]
            
            for req_config in required_configs:
                if req_config not in config_names:
                    errores.append(f"[ERROR] Configuracion '{req_config}' no encontrada")
                else:
                    print(f"[OK] Configuracion '{req_config}' encontrada")
            
            # Verificar que todas las configuraciones tengan 'request'
            for config in configs:
                name = config.get('name', 'Sin nombre')
                if 'request' not in config:
                    errores.append(f"[ERROR] Configuracion '{name}' no tiene atributo 'request'")
                else:
                    print(f"[OK] Configuracion '{name}' tiene 'request': {config['request']}")
            
            # Verificar compounds
            compounds = launch_config.get('compounds', [])
            if compounds:
                for compound in compounds:
                    compound_name = compound.get('name', 'Sin nombre')
                    print(f"[OK] Compound '{compound_name}' encontrado")
                    
                    # Verificar que las configuraciones del compound existan
                    compound_configs = compound.get('configurations', [])
                    for comp_config in compound_configs:
                        if comp_config not in config_names:
                            errores.append(f"[ERROR] Compound '{compound_name}' referencia configuracion inexistente: '{comp_config}'")
                        else:
                            print(f"  [OK] Referencia valida: '{comp_config}'")
            
        except json.JSONDecodeError as e:
            errores.append(f"[ERROR] Error en formato JSON de launch.json: {e}")
        except Exception as e:
            errores.append(f"[ERROR] Error leyendo launch.json: {e}")
    
    # Verificar tasks.json
    tasks_file = vscode_dir / "tasks.json"
    if not tasks_file.exists():
        warnings.append("[WARNING] Archivo .vscode/tasks.json no existe")
    else:
        try:
            with open(tasks_file, 'r', encoding='utf-8') as f:
                tasks_config = json.load(f)
            
            tasks = tasks_config.get('tasks', [])
            task_labels = [t.get('label') for t in tasks]
            
            # Verificar tarea específica
            if "start-fullstack-environment" in task_labels:
                print("[OK] Tarea 'start-fullstack-environment' encontrada")
            else:
                warnings.append("[WARNING] Tarea 'start-fullstack-environment' no encontrada")
                
        except json.JSONDecodeError as e:
            warnings.append(f"[WARNING] Error en formato JSON de tasks.json: {e}")
        except Exception as e:
            warnings.append(f"[WARNING] Error leyendo tasks.json: {e}")
    
    # Verificar extensions.json
    extensions_file = vscode_dir / "extensions.json"
    if not extensions_file.exists():
        warnings.append("[WARNING] Archivo .vscode/extensions.json no existe")
    else:
        try:
            with open(extensions_file, 'r', encoding='utf-8') as f:
                extensions_config = json.load(f)
            
            recommendations = extensions_config.get('recommendations', [])
            essential_extensions = [
                "ms-python.python",
                "ms-python.debugpy",
                "ms-vscode.js-debug"
            ]
            
            for ext in essential_extensions:
                if ext in recommendations:
                    print(f"[OK] Extension esencial '{ext}' recomendada")
                else:
                    warnings.append(f"[WARNING] Extension esencial '{ext}' no esta en recomendaciones")
                    
        except json.JSONDecodeError as e:
            warnings.append(f"[WARNING] Error en formato JSON de extensions.json: {e}")
        except Exception as e:
            warnings.append(f"[WARNING] Error leyendo extensions.json: {e}")
    
    # Verificar que existe el orquestador
    orquestador_path = Path("devtools/orquestador_desarrollo.py")
    if not orquestador_path.exists():
        errores.append("[ERROR] Archivo devtools/orquestador_desarrollo.py no encontrado")
    else:
        print("[OK] Orquestador de desarrollo encontrado")
    
    return errores, warnings

def main():
    """Función principal"""
    print("=" * 60)
    print("VALIDADOR DE CONFIGURACION VS CODE DEBUG")
    print("=" * 60)
    
    errores, warnings = validar_configuracion()
    
    print("\n" + "=" * 60)
    print("RESULTADO DE LA VALIDACION")
    print("=" * 60)
    
    if not errores and not warnings:
        print("¡PERFECTO! La configuracion esta completamente correcta.")
        print("\n[OK] Puedes usar F5 con 'FullStack Debug - Ambos simultaneamente'")
        
    elif not errores:
        print("[OK] Configuracion VALIDA (con advertencias menores)")
        print("\nAdvertencias:")
        for warning in warnings:
            print(f"   {warning}")
            
    else:
        print("[ERROR] Configuracion con ERRORES")
        print("\nErrores criticos:")
        for error in errores:
            print(f"   {error}")
        
        if warnings:
            print("\nAdvertencias:")
            for warning in warnings:
                print(f"   {warning}")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()
