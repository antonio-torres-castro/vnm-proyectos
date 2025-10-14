#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verificador Completo de Configuracion - Post Refactorizacion
Ejecuta todas las verificaciones necesarias despues de los movimientos de archivos
Autor: MiniMax Agent
"""

import subprocess
import sys
import os
from pathlib import Path

# Configurar encoding para Windows
if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except:
        pass

def ejecutar_script(script_name, descripcion):
    """Ejecuta un script y muestra el resultado"""
    print(f"\n{'='*60}")
    print(f"{descripcion}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run([sys.executable, script_name], 
                              capture_output=True, text=True, cwd=os.getcwd())
        
        if result.returncode == 0:
            print(result.stdout)
            return True
        else:
            print(f"[ERROR] Error ejecutando {script_name}:")
            print(result.stderr)
            print(result.stdout)
            return False
            
    except Exception as e:
        print(f"[ERROR] Excepcion ejecutando {script_name}: {e}")
        return False

def main():
    """Funcion principal de verificacion completa"""
    print("VERIFICADOR COMPLETO DE CONFIGURACION")
    print("="*60)
    print("Verificando configuracion despues de la refactorizacion...")
    print("Autor: MiniMax Agent")
    print(f"Ejecutando desde: {os.getcwd()}")
    print()
    
    resultados = {}
    
    # 1. Verificar archivos movidos
    resultados['archivos'] = ejecutar_script(
        'validar_archivos_movidos.py',
        'VALIDANDO ARCHIVOS MOVIDOS'
    )
    
    # 2. Verificar configuracion VS Code instalada
    resultados['vscode'] = ejecutar_script(
        'verificar_vscode_instalado.py',
        'VERIFICANDO CONFIGURACION VS CODE'
    )
    
    # 3. Validar configuracion VS Code
    resultados['vscode_validacion'] = ejecutar_script(
        'validar_configuracion_vscode.py',
        'VALIDANDO CONFIGURACION DE DEBUG'
    )
    
    # Resumen final
    print(f"\n{'='*60}")
    print("RESUMEN FINAL DE VERIFICACION")
    print(f"{'='*60}")
    
    todo_ok = True
    for nombre, resultado in resultados.items():
        status = "[OK]" if resultado else "[ERROR]"
        print(f"{status} {nombre.upper()}")
        if not resultado:
            todo_ok = False
    
    print(f"\n{'='*60}")
    if todo_ok:
        print("CONFIGURACION COMPLETA Y CORRECTA!")
        print("[OK] Todos los archivos estan en su lugar")
        print("[OK] VS Code esta configurado correctamente")
        print("[OK] Debug esta listo para usar")
        
        print(f"\n{'='*60}")
        print("INSTRUCCIONES PARA CONTINUAR:")
        print(f"{'='*60}")
        print()
        print("1. DESCARGAR PROYECTO:")
        print("   - Descarga toda la carpeta 'vnm-proyectos'")
        print("   - Manten la estructura de carpetas")
        print()
        print("2. CONFIGURAR VS CODE:")
        print("   - Abre VS Code en la carpeta 'vnm-proyectos'")
        print("   - Acepta instalar las extensiones recomendadas")
        print()
        print("3. INICIAR DOCKER:")
        print("   - Asegurate de que Docker Desktop este ejecutandose")
        print("   - Verifica que los puertos 3000 y 8000 esten disponibles")
        print()
        print("4. DEBUGGING:")
        print("   - Presiona F5 en VS Code")
        print("   - Selecciona: 'FullStack Debug - Ambos simultaneamente'")
        print("   - El navegador se abrira automaticamente")
        print()
        print("5. COMANDOS ALTERNATIVOS (desde vnm-proyectos/):")
        print("   - PowerShell: '.\\comandos-desarrollo.ps1' y luego 'Dev-Start'")
        print("   - Python: 'python automate\\devtools\\orquestador_desarrollo.py'")
        print()
        print("6. VERIFICAR CONFIGURACION (si hay problemas):")
        print("   - Desde vnm-proyectos\\automate\\:")
        print("   - 'python verificar_vscode_instalado.py'")
        print("   - 'python validar_configuracion_vscode.py'")
        
    else:
        print("[ERROR] SE ENCONTRARON PROBLEMAS")
        print("Revisa los errores mostrados arriba")
        print("Contacta al desarrollador si persisten los problemas")
    
    print(f"\n{'='*60}")
    return 0 if todo_ok else 1

if __name__ == "__main__":
    try:
        exit_code = main()
        exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n[WARNING] Verificacion cancelada por el usuario")
        exit(1)
    except Exception as e:
        print(f"\n[ERROR] ERROR INESPERADO: {e}")
        exit(1)
