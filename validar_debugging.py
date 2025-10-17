#!/usr/bin/env python3
"""
Validador de Configuracion de Debugging
Verifica que el entorno este configurado correctamente para debugging integrado
"""
import json
import subprocess
from pathlib import Path

def check_file_exists(file_path, description):
    """Verificar que un archivo exista"""
    if Path(file_path).exists():
        print(f"[OK] {description}: {file_path}")
        return True
    else:
        print(f"[FALLO] {description}: {file_path} - NO ENCONTRADO")
        return False

def check_vscode_config():
    """Verificar configuracion de VS Code"""
    print("=== VERIFICACION CONFIGURACION VS CODE ===")
    
    config_files = [
        ("_vscode/launch.json", "Configuracion de debug (backup)"),
        (".vscode/launch.json", "Configuracion de debug (activo)"),
        ("_vscode/tasks.json", "Tareas automatizadas (backup)"),
        (".vscode/tasks.json", "Tareas automatizadas (activo)"),
    ]
    
    all_good = True
    for file_path, desc in config_files:
        if not check_file_exists(file_path, desc):
            all_good = False
    
    return all_good

def check_launch_config():
    """Verificar configuraciones de launch"""
    print("\n=== VERIFICACION CONFIGURACIONES DE LAUNCH ===")
    
    try:
        with open(".vscode/launch.json", "r") as f:
            launch_config = json.load(f)
        
        configs = launch_config.get("configurations", [])
        config_names = [config["name"] for config in configs]
        
        required_configs = [
            "Backend Debug (Container)",
            "FullStack Debug (Smart)"
        ]
        
        all_good = True
        for config_name in required_configs:
            if config_name in config_names:
                print(f"[OK] Configuracion encontrada: {config_name}")
            else:
                print(f"[FALLO] Configuracion faltante: {config_name}")
                all_good = False
        
        # Verificar que FullStack Debug (Smart) use la tarea correcta
        smart_config = next((c for c in configs if c["name"] == "FullStack Debug (Smart)"), None)
        if smart_config:
            if smart_config.get("preLaunchTask") == "start-development-environment":
                print("[OK] FullStack Debug (Smart) usa tarea inteligente")
            else:
                print("[FALLO] FullStack Debug (Smart) no usa tarea inteligente")
                all_good = False
        
        return all_good
        
    except Exception as e:
        print(f"[FALLO] Error leyendo launch.json: {e}")
        return False

def check_tasks_config():
    """Verificar configuracion de tareas"""
    print("\n=== VERIFICACION CONFIGURACION DE TAREAS ===")
    
    try:
        with open(".vscode/tasks.json", "r") as f:
            tasks_config = json.load(f)
        
        tasks = tasks_config.get("tasks", [])
        task_labels = [task["label"] for task in tasks]
        
        required_tasks = [
            "start-containers",
            "start-development-environment",
            "stop-development-environment"
        ]
        
        all_good = True
        for task_label in required_tasks:
            if task_label in task_labels:
                print(f"[OK] Tarea encontrada: {task_label}")
            else:
                print(f"[FALLO] Tarea faltante: {task_label}")
                all_good = False
        
        # Verificar que start-containers use modo debug
        start_task = next((t for t in tasks if t["label"] == "start-containers"), None)
        if start_task:
            args = start_task.get("args", [])
            if "start-debug" in args:
                print("[OK] start-containers usa modo debug")
            else:
                print("[FALLO] start-containers NO usa modo debug")
                all_good = False
        
        return all_good
        
    except Exception as e:
        print(f"[FALLO] Error leyendo tasks.json: {e}")
        return False

def check_docker_compose():
    """Verificar archivos docker-compose"""
    print("\n=== VERIFICACION DOCKER COMPOSE ===")
    
    compose_files = [
        ("docker-compose.yml", "Configuracion produccion"),
        ("docker-compose.debug.yml", "Configuracion debug")
    ]
    
    all_good = True
    for file_path, desc in compose_files:
        if not check_file_exists(file_path, desc):
            all_good = False
    
    return all_good

def check_automation_scripts():
    """Verificar scripts de automatizacion"""
    print("\n=== VERIFICACION SCRIPTS DE AUTOMATIZACION ===")
    
    scripts = [
        ("automate/vnm_automate.py", "Script maestro de automatizacion"),
        ("devtools/orquestador_desarrollo.py", "Orquestador inteligente"),
        ("docker_manager.py", "Manager basico de containers")
    ]
    
    all_good = True
    for file_path, desc in scripts:
        if not check_file_exists(file_path, desc):
            all_good = False
    
    return all_good

def main():
    """Funcion principal"""
    print("VALIDADOR DE CONFIGURACION DE DEBUGGING")
    print("=" * 60)
    
    checks = [
        check_vscode_config,
        check_launch_config,
        check_tasks_config,
        check_docker_compose,
        check_automation_scripts
    ]
    
    all_passed = True
    for check in checks:
        if not check():
            all_passed = False
        print()
    
    print("=" * 60)
    if all_passed:
        print("RESULTADO: CONFIGURACION CORRECTA")
        print("\nPara iniciar debugging:")
        print("1. Abrir VS Code")
        print("2. Ir a Debug panel (Ctrl+Shift+D)")
        print("3. Seleccionar 'FullStack Debug (Smart)'")
        print("4. Presionar F5")
        print("\nEl entorno se levantara automaticamente en modo debug.")
    else:
        print("RESULTADO: CONFIGURACION INCOMPLETA")
        print("\nExecutar para reparar:")
        print("python automate/vnm_automate.py vscode-install")
        
    return 0 if all_passed else 1

if __name__ == "__main__":
    exit(main())