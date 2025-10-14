#!/usr/bin/env python3
"""
Script de prueba para validar la configuración de VS Code
"""

import json
import os
import subprocess
from pathlib import Path

def test_vscode_configuration():
    """Prueba la configuración de VS Code"""
    print("🔍 Testeando configuración de VS Code FullStack Debug")
    print("=" * 60)
    
    errors = []
    warnings = []
    
    # 1. Verificar archivos de configuración VS Code
    print("\n1. Verificando archivos de configuración...")
    
    vscode_files = [
        '../.vscode/launch.json',
        '../.vscode/tasks.json', 
        '../.vscode/settings.json',
        '../.vscode/extensions.json'
    ]
    
    for file_path in vscode_files:
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r') as f:
                    json.load(f)
                print(f"✅ {file_path} - JSON válido")
            except json.JSONDecodeError as e:
                errors.append(f"❌ {file_path} - JSON inválido: {e}")
        else:
            errors.append(f"❌ {file_path} - No encontrado")
    
    # 2. Verificar archivos del proyecto
    print("\n2. Verificando archivos del proyecto...")
    
    project_files = [
        'backend/app/main.py',
        'frontend/package.json',
        'devtools/orquestador_desarrollo.py',
        '../docker-compose.debug.yml'
    ]
    
    for file_path in project_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path} - Existe")
        else:
            errors.append(f"❌ {file_path} - No encontrado")
    
    # 3. Verificar configuraciones específicas
    print("\n3. Verificando configuraciones específicas...")
    
    try:
        with open('../.vscode/launch.json', 'r') as f:
            launch_config = json.load(f)
        
        # Verificar que existe configuración FullStack Debug en compounds
        compounds = launch_config.get('compounds', [])
        fullstack_compound = None
        for compound in compounds:
            if compound.get('name') == 'FullStack Debug':
                fullstack_compound = compound
                break
        
        if fullstack_compound:
            print("✅ Configuración 'FullStack Debug' encontrada en compounds")
            
            # Verificar que las configuraciones referenciadas existen
            configurations = launch_config.get('configurations', [])
            config_names = [c.get('name') for c in configurations]
            
            for ref_config in fullstack_compound.get('configurations', []):
                if ref_config in config_names:
                    print(f"✅ Configuración referenciada '{ref_config}' existe")
                else:
                    errors.append(f"❌ Configuración referenciada '{ref_config}' no encontrada")
        else:
            errors.append("❌ Configuración 'FullStack Debug' no encontrada en compounds")
    
    except Exception as e:
        errors.append(f"❌ Error al verificar launch.json: {e}")
    
    # 4. Verificar tareas
    print("\n4. Verificando tareas...")
    
    try:
        with open('../.vscode/tasks.json', 'r') as f:
            tasks_config = json.load(f)
        
        task_names = [task.get('label') for task in tasks_config.get('tasks', [])]
        required_tasks = [
            'start-frontend',
            'start-backend-dependencies', 
            'start-fullstack-environment'
        ]
        
        for task_name in required_tasks:
            if task_name in task_names:
                print(f"✅ Tarea '{task_name}' configurada")
            else:
                errors.append(f"❌ Tarea '{task_name}' no encontrada")
    
    except Exception as e:
        errors.append(f"❌ Error al verificar tasks.json: {e}")
    
    # 5. Limitaciones del entorno sandbox
    print("\n5. Limitaciones del entorno sandbox...")
    warnings.append("⚠️  Este entorno no tiene Docker - no se pueden iniciar servicios reales")
    warnings.append("⚠️  Este entorno no tiene VS Code - no se puede probar la depuración real")
    warnings.append("⚠️  Este entorno no tiene Chrome - no se puede depurar frontend")
    
    # Resumen
    print("\n" + "=" * 60)
    print("📊 RESUMEN DE LA PRUEBA")
    print("=" * 60)
    
    if not errors:
        print("🎉 ¡CONFIGURACIÓN VÁLIDA!")
        print("✅ Todos los archivos de configuración están correctos")
        print("✅ Todas las referencias son válidas") 
        print("✅ La configuración FullStack Debug está bien formada")
    else:
        print("❌ SE ENCONTRARON ERRORES:")
        for error in errors:
            print(f"   {error}")
    
    if warnings:
        print("\n⚠️  ADVERTENCIAS:")
        for warning in warnings:
            print(f"   {warning}")
    
    print("\n🚀 PARA PROBAR EN TU ENTORNO LOCAL:")
    print("   1. Reinicia VS Code")
    print("   2. Instala las extensiones recomendadas")
    print("   3. Presiona F5 y selecciona 'FullStack Debug'")
    print("   4. VS Code debería iniciar automáticamente:")
    print("      - PostgreSQL y Redis (Docker)")
    print("      - Backend FastAPI")
    print("      - Frontend React")
    print("      - Depurador para ambos")

if __name__ == "__main__":
    test_vscode_configuration()
