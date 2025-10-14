#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verificador de Configuración VS Code Instalada
Verifica que la configuración de debugging esté correctamente instalada en .vscode/
Autor: MiniMax Agent
"""

import json
import os
import sys
from pathlib import Path
import platform

# Configurar encoding para Windows
if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except:
        pass

def verificar_configuracion_instalada():
    """Verifica que la configuración de VS Code esté correctamente instalada"""
    
    print("Verificando configuracion instalada de VS Code...")
    
    errores = []
    warnings = []
    sistema = platform.system()
    
    # Verificar que existe la carpeta .vscode en vnm-proyectos
    vscode_dir = Path("../.vscode")
    if not vscode_dir.exists():
        errores.append("[ERROR] Carpeta .vscode no existe en vnm-proyectos/ - Ejecuta 'python instalar_vscode_config.py'")
        return errores, warnings
    
    print(f"[OK] Sistema detectado: {sistema}")
    print(f"[OK] Carpeta .vscode encontrada")
    
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
            
            # Verificar que existan las configuraciones corregidas
            required_configs = [
                "Frontend Debug",
                "Backend Debug", 
                "FullStack Debug - Ambos simultáneamente"
            ]
            
            for req_config in required_configs:
                if req_config not in config_names:
                    errores.append(f"[ERROR] Configuracion '{req_config}' no encontrada")
                else:
                    print(f"[OK] Configuracion '{req_config}' instalada")
            
            # Verificar que todas las configuraciones tengan 'request' (esto solucionaba el error)
            configs_sin_request = []
            for config in configs:
                name = config.get('name', 'Sin nombre')
                if 'request' not in config:
                    configs_sin_request.append(name)
                else:
                    print(f"[OK] '{name}' tiene 'request': {config['request']}")
            
            if configs_sin_request:
                errores.append(f"[ERROR] Configuraciones sin 'request': {', '.join(configs_sin_request)}")
            else:
                print("[OK] Todas las configuraciones tienen atributo 'request' (error solucionado)")
            
            # Verificar compounds
            compounds = launch_config.get('compounds', [])
            if compounds:
                for compound in compounds:
                    compound_name = compound.get('name', 'Sin nombre')
                    print(f"[OK] Compound '{compound_name}' instalado")
            
        except json.JSONDecodeError as e:
            errores.append(f"[ERROR] Error en formato JSON de launch.json: {e}")
        except Exception as e:
            errores.append(f"[ERROR] Error leyendo launch.json: {e}")
    
    # Verificar tasks.json
    tasks_file = vscode_dir / "tasks.json"
    if not tasks_file.exists():
        errores.append("[ERROR] Archivo .vscode/tasks.json no existe")
    else:
        try:
            with open(tasks_file, 'r', encoding='utf-8') as f:
                tasks_config = json.load(f)
            
            tasks = tasks_config.get('tasks', [])
            task_labels = [t.get('label') for t in tasks]
            
            # Verificar tarea específica
            if "start-fullstack-environment" in task_labels:
                print("[OK] Tarea 'start-fullstack-environment' instalada")
            else:
                errores.append("[ERROR] Tarea 'start-fullstack-environment' no encontrada")
                
        except json.JSONDecodeError as e:
            errores.append(f"[ERROR] Error en formato JSON de tasks.json: {e}")
        except Exception as e:
            errores.append(f"[ERROR] Error leyendo tasks.json: {e}")
    
    # Verificar extensions.json
    extensions_file = vscode_dir / "extensions.json"
    if not extensions_file.exists():
        warnings.append("⚠️  Archivo .vscode/extensions.json no existe")
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
                    print(f"[OK] Extension '{ext}' recomendada")
                else:
                    warnings.append(f"⚠️  Extensión '{ext}' no está en recomendaciones")
                    
        except json.JSONDecodeError as e:
            warnings.append(f"⚠️  Error en formato JSON de extensions.json: {e}")
        except Exception as e:
            warnings.append(f"⚠️  Error leyendo extensions.json: {e}")
    
    # Verificar configuración específica para Windows
    if sistema == "Windows":
        settings_file = vscode_dir / "settings.json"
        if settings_file.exists():
            try:
                with open(settings_file, 'r', encoding='utf-8') as f:
                    settings = json.load(f)
                
                python_path = settings.get("python.defaultInterpreterPath", "")
                if "Scripts\\python.exe" in python_path or ".venv" in python_path:
                    print("[OK] Configuracion Python ajustada para Windows")
                else:
                    warnings.append("⚠️  Configuración Python puede requerir ajuste para Windows")
                    
                terminal_profile = settings.get("terminal.integrated.defaultProfile.windows", "")
                if terminal_profile == "PowerShell":
                    print("[OK] Terminal configurado para PowerShell")
                    
            except Exception as e:
                warnings.append(f"⚠️  No se pudo verificar configuración Windows: {e}")
    
    # Verificar que existe el orquestador
    orquestador_path = Path("devtools/orquestador_desarrollo.py")
    if not orquestador_path.exists():
        errores.append("[ERROR] Archivo devtools/orquestador_desarrollo.py no encontrado")
    else:
        print("[OK] Orquestador de desarrollo encontrado")
    
    return errores, warnings

def mostrar_siguiente_paso():
    """Muestra las instrucciones del siguiente paso"""
    print("\n" + "="*60)
    print("PROXIMOS PASOS PARA USAR VS CODE DEBUG")
    print("="*60)
    
    print("\n1. Abre VS Code en este directorio:")
    print("   code .")
    
    print("\n2. Instala las extensiones recomendadas:")
    print("   VS Code te preguntará automáticamente")
    print("   O ve a Extensions > Show Recommended Extensions")
    
    print("\n3. Asegurate que Docker Desktop este ejecutandose")
    
    print("\n4. Presiona F5 para debugging:")
    print("   Selecciona: 'FullStack Debug - Ambos simultáneamente'")
    
    print("\n5. Espera a que inicie el entorno:")
    print("   Verás mensajes en la terminal de VS Code")
    print("   El navegador se abrirá automáticamente en http://localhost:3000")
    
    print("\nDEBUGGING LISTO:")
    print("   • Pon breakpoints en tu código Python")
    print("   • Usa F10, F11 para step debugging")
    print("   • Inspecciona variables en el panel Debug")

def main():
    """Función principal"""
    print("=" * 60)
    print("VERIFICADOR DE CONFIGURACION VS CODE INSTALADA")
    print("=" * 60)
    
    errores, warnings = verificar_configuracion_instalada()
    
    print("\n" + "=" * 60)
    print("RESULTADO DE LA VERIFICACION")
    print("=" * 60)
    
    if not errores and not warnings:
        print("¡PERFECTO! La configuracion esta completamente instalada y correcta.")
        print("\n[OK] El error 'Attribute request is missing' esta solucionado")
        mostrar_siguiente_paso()
        
    elif not errores:
        print("[OK] Configuracion INSTALADA correctamente (con advertencias menores)")
        print("\n🟡 Advertencias:")
        for warning in warnings:
            print(f"   {warning}")
        mostrar_siguiente_paso()
            
    else:
        print("[ERROR] Configuracion con PROBLEMAS")
        print("\n🔴 Errores críticos:")
        for error in errores:
            print(f"   {error}")
        
        if warnings:
            print("\n🟡 Advertencias:")
            for warning in warnings:
                print(f"   {warning}")
        
        print("\nSOLUCION:")
        print("   Ejecuta: python instalar_vscode_config.py")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()
