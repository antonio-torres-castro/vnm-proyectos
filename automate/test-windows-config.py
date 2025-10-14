#!/usr/bin/env python3
"""
Script de prueba para validar la configuración de Windows
"""

import os
import json
import platform
import subprocess
from pathlib import Path

def test_windows_configuration():
    """Prueba la configuración específica para Windows"""
    print("🔍 Testeando configuración para Windows")
    print("=" * 60)
    
    errors = []
    warnings = []
    
    # 1. Verificar plataforma
    print("\n1. Verificando plataforma...")
    current_platform = platform.system()
    print(f"✅ Sistema detectado: {current_platform}")
    
    if current_platform != "Windows":
        warnings.append(f"⚠️  Este test está diseñado para Windows, pero detectó: {current_platform}")
    
    # 2. Verificar archivos de comandos para Windows
    print("\n2. Verificando archivos de comandos para Windows...")
    
    windows_files = [
        'comandos-desarrollo.ps1',
        'comandos-desarrollo.bat'
    ]
    
    for file_path in windows_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path} - Existe")
            
            # Verificar contenido básico
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                if 'dev-start' in content.lower() or 'Dev-Start' in content:
                    print(f"✅ {file_path} - Contiene comandos básicos")
                else:
                    warnings.append(f"⚠️  {file_path} - Posible contenido incompleto")
        else:
            errors.append(f"❌ {file_path} - No encontrado")
    
    # 3. Verificar archivos universales
    print("\n3. Verificando archivos universales...")
    
    universal_files = [
        'devtools/orquestador_desarrollo.py',
        '../.vscode/launch.json',
        '../.vscode/tasks.json',
        '../docker-compose.debug.yml'
    ]
    
    for file_path in universal_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path} - Existe")
        else:
            errors.append(f"❌ {file_path} - No encontrado")
    
    # 4. Verificar estructura de comandos PowerShell
    print("\n4. Verificando estructura de PowerShell...")
    
    ps1_file = 'comandos-desarrollo.ps1'
    if os.path.exists(ps1_file):
        with open(ps1_file, 'r', encoding='utf-8') as f:
            ps1_content = f.read()
        
        # Verificar funciones principales
        required_functions = [
            'Dev-Start',
            'Dev-Status', 
            'Dev-Stop',
            'Dev-Logs',
            'Show-DevHelp'
        ]
        
        for func in required_functions:
            if f"function {func}" in ps1_content:
                print(f"✅ Función '{func}' definida")
            else:
                errors.append(f"❌ Función '{func}' no encontrada en PowerShell")
    
    # 5. Verificar estructura de comandos Batch
    print("\n5. Verificando estructura de Batch...")
    
    bat_file = 'comandos-desarrollo.bat'
    if os.path.exists(bat_file):
        with open(bat_file, 'r', encoding='utf-8') as f:
            bat_content = f.read()
        
        # Verificar labels principales
        required_labels = [
            ':dev_start',
            ':dev_status',
            ':dev_stop',
            ':dev_logs',
            ':show_help'
        ]
        
        for label in required_labels:
            if label in bat_content:
                print(f"✅ Label '{label}' definido")
            else:
                errors.append(f"❌ Label '{label}' no encontrado en Batch")
    
    # 6. Verificar herramientas necesarias
    print("\n6. Verificando herramientas necesarias...")
    
    tools = [
        ('python', 'python --version'),
        ('docker', 'docker --version'),
        ('docker-compose', 'docker-compose --version')
    ]
    
    for tool_name, command in tools:
        try:
            result = subprocess.run(command.split(), capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                version = result.stdout.strip()
                print(f"✅ {tool_name} - {version}")
            else:
                warnings.append(f"⚠️  {tool_name} - Comando falló: {result.stderr.strip()}")
        except (subprocess.TimeoutExpired, FileNotFoundError, subprocess.CalledProcessError, PermissionError) as e:
            if current_platform != "Windows" and tool_name in ['docker', 'docker-compose']:
                warnings.append(f"⚠️  {tool_name} - No disponible en entorno sandbox (normal)")
            else:
                warnings.append(f"⚠️  {tool_name} - No disponible o error: {e}")
    
    # 7. Verificar documentación para Windows
    print("\n7. Verificando documentación para Windows...")
    
    docs = [
        'FLUJO_DESARROLLO_WINDOWS.md',
        'INICIO_RAPIDO_WINDOWS.md',
        'RESUMEN_FINAL_FLUJO_DESARROLLO.md'
    ]
    
    for doc in docs:
        if os.path.exists(doc):
            print(f"✅ {doc} - Existe")
            
            # Verificar que contiene información de Windows
            with open(doc, 'r', encoding='utf-8') as f:
                content = f.read()
                if 'PowerShell' in content or 'Windows' in content or '.bat' in content:
                    print(f"✅ {doc} - Contiene información de Windows")
                else:
                    warnings.append(f"⚠️  {doc} - Falta información específica de Windows")
        else:
            errors.append(f"❌ {doc} - No encontrado")
    
    # 8. Verificar compatibilidad de paths
    print("\n8. Verificando compatibilidad de paths...")
    
    # Verificar que no hay paths hardcodeados de Linux
    check_files = ['comandos-desarrollo.ps1', 'comandos-desarrollo.bat']
    linux_patterns = ['/usr/', '/bin/', '/etc/', '~/', '$HOME']
    
    for file_path in check_files:
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            found_linux_paths = [pattern for pattern in linux_patterns if pattern in content]
            if found_linux_paths:
                warnings.append(f"⚠️  {file_path} - Contiene paths de Linux: {found_linux_paths}")
            else:
                print(f"✅ {file_path} - Paths compatibles con Windows")
    
    # Resumen
    print("\n" + "=" * 60)
    print("📊 RESUMEN DE LA PRUEBA PARA WINDOWS")
    print("=" * 60)
    
    if not errors:
        print("🎉 ¡CONFIGURACIÓN WINDOWS VÁLIDA!")
        print("✅ Todos los archivos necesarios están presentes")
        print("✅ Scripts PowerShell y Batch están bien formados")
        print("✅ Documentación específica para Windows disponible")
    else:
        print("❌ SE ENCONTRARON ERRORES:")
        for error in errors:
            print(f"   {error}")
    
    if warnings:
        print("\n⚠️  ADVERTENCIAS:")
        for warning in warnings:
            print(f"   {warning}")
    
    print("\n🚀 PARA USAR EN WINDOWS:")
    print("\n🟦 OPCIÓN A: PowerShell (Recomendado)")
    print("   1. Abrir PowerShell en el directorio del proyecto")
    print("   2. Ejecutar: . .\\comandos-desarrollo.ps1")
    print("   3. Usar comandos: Dev-Start, Dev-Status, Dev-Stop")
    
    print("\n🟨 OPCIÓN B: Command Prompt")
    print("   1. Abrir CMD en el directorio del proyecto") 
    print("   2. Usar comandos: comandos-desarrollo.bat start")
    
    print("\n🎯 OPCIÓN C: VS Code")
    print("   1. Abrir VS Code en el proyecto")
    print("   2. Presionar F5 → Seleccionar 'FullStack Debug'")
    
    print("\n📚 DOCUMENTACIÓN:")
    print("   - INICIO_RAPIDO_WINDOWS.md - Guía de inicio rápido")
    print("   - FLUJO_DESARROLLO_WINDOWS.md - Documentación completa")

if __name__ == "__main__":
    test_windows_configuration()
