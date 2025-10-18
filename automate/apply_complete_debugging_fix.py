#!/usr/bin/env python3
"""
Script completo para corregir la configuracion de debugging del frontend.
Crea automaticamente todos los archivos de configuracion necesarios.
"""

import os
import sys
import json
import shutil
from pathlib import Path


def crear_backup(archivo):
    """Crea backup de un archivo antes de modificarlo."""
    if os.path.exists(archivo):
        backup = archivo + '.backup'
        shutil.copy2(archivo, backup)
        print(f"✓ Backup creado: {backup}")


def crear_directorio_seguro(directorio):
    """Crea un directorio de forma segura."""
    try:
        Path(directorio).mkdir(parents=True, exist_ok=True)
        print(f"✓ Directorio creado/verificado: {directorio}")
        return True
    except Exception as e:
        print(f"❌ Error creando directorio {directorio}: {e}")
        return False


def escribir_archivo_json(ruta, contenido):
    """Escribe un archivo JSON de forma segura."""
    try:
        with open(ruta, 'w', encoding='utf-8') as f:
            json.dump(contenido, f, indent=2, ensure_ascii=False)
        print(f"✓ Archivo JSON creado: {ruta}")
        return True
    except Exception as e:
        print(f"❌ Error escribiendo {ruta}: {e}")
        return False


def escribir_archivo_texto(ruta, contenido):
    """Escribe un archivo de texto de forma segura."""
    try:
        with open(ruta, 'w', encoding='utf-8') as f:
            f.write(contenido)
        print(f"✓ Archivo creado: {ruta}")
        return True
    except Exception as e:
        print(f"❌ Error escribiendo {ruta}: {e}")
        return False


def crear_configuraciones_vscode():
    """Crea todas las configuraciones de VS Code necesarias."""
    
    # Configuracion para vnm-proyectos/.vscode/ (root)
    root_vscode_dir = "_vscode"
    if not crear_directorio_seguro(root_vscode_dir):
        return False
    
    # launch.json para root
    root_launch_config = {
        "version": "0.2.0",
        "configurations": [
            {
                "name": "FullStack Debug (Complete)",
                "type": "node",
                "request": "attach",
                "address": "localhost",
                "port": 24678,
                "localRoot": "${workspaceFolder}/frontend",
                "remoteRoot": "/app",
                "protocol": "inspector",
                "restart": True,
                "sourceMaps": True,
                "skipFiles": [
                    "<node_internals>/**"
                ],
                "outFiles": [
                    "${workspaceFolder}/frontend/dist/**/*.js"
                ],
                "resolveSourceMapLocations": [
                    "${workspaceFolder}/frontend/**",
                    "!**/node_modules/**"
                ]
            }
        ]
    }
    
    # settings.json para root
    root_settings_config = {
        "python.defaultInterpreterPath": "./venv/Scripts/python.exe",
        "python.terminal.activateEnvironment": True,
        "files.encoding": "utf8",
        "files.autoSave": "afterDelay",
        "editor.formatOnSave": True,
        "python.formatting.provider": "black",
        "python.linting.enabled": True,
        "python.linting.pylintEnabled": True,
        "typescript.preferences.includePackageJsonAutoImports": "auto",
        "javascript.preferences.includePackageJsonAutoImports": "auto",
        "debug.console.fontSize": 14,
        "debug.console.fontFamily": "Consolas, 'Courier New', monospace"
    }
    
    # tasks.json para root
    root_tasks_config = {
        "version": "2.0.0",
        "tasks": [
            {
                "label": "Iniciar Frontend Debug",
                "type": "shell",
                "command": "docker-compose",
                "args": ["-f", "docker-compose.debug.yml", "up", "-d", "frontend"],
                "group": "build",
                "presentation": {
                    "echo": True,
                    "reveal": "always",
                    "focus": False,
                    "panel": "shared"
                },
                "problemMatcher": []
            },
            {
                "label": "Detener Frontend Debug",
                "type": "shell",
                "command": "docker-compose",
                "args": ["-f", "docker-compose.debug.yml", "down"],
                "group": "build",
                "presentation": {
                    "echo": True,
                    "reveal": "always",
                    "focus": False,
                    "panel": "shared"
                },
                "problemMatcher": []
            }
        ]
    }
    
    # extensions.json para root
    root_extensions_config = {
        "recommendations": [
            "ms-python.python",
            "ms-python.black-formatter",
            "ms-vscode.vscode-typescript-next",
            "bradlc.vscode-tailwindcss",
            "esbenp.prettier-vscode"
        ]
    }
    
    # Crear archivos para root
    if not escribir_archivo_json(f"{root_vscode_dir}/launch.json", root_launch_config):
        return False
    if not escribir_archivo_json(f"{root_vscode_dir}/settings.json", root_settings_config):
        return False
    if not escribir_archivo_json(f"{root_vscode_dir}/tasks.json", root_tasks_config):
        return False
    if not escribir_archivo_json(f"{root_vscode_dir}/extensions.json", root_extensions_config):
        return False
    
    # Configuracion para frontend/.vscode/
    frontend_vscode_dir = "frontend/_vscode"
    if not crear_directorio_seguro(frontend_vscode_dir):
        return False
    
    # launch.json para frontend (vacio, se usa el del root)
    frontend_launch_config = {
        "version": "0.2.0",
        "configurations": []
    }
    
    # settings.json para frontend
    frontend_settings_config = {
        "typescript.preferences.includePackageJsonAutoImports": "auto",
        "javascript.preferences.includePackageJsonAutoImports": "auto",
        "editor.formatOnSave": True,
        "editor.defaultFormatter": "esbenp.prettier-vscode",
        "emmet.includeLanguages": {
            "javascript": "javascriptreact",
            "typescript": "typescriptreact"
        }
    }
    
    # Crear archivos para frontend
    if not escribir_archivo_json(f"{frontend_vscode_dir}/launch.json", frontend_launch_config):
        return False
    if not escribir_archivo_json(f"{frontend_vscode_dir}/settings.json", frontend_settings_config):
        return False
    
    return True


def actualizar_package_json():
    """Actualiza package.json para habilitar debugging."""
    package_path = "frontend/package.json"
    
    if not os.path.exists(package_path):
        print(f"❌ No se encontro {package_path}")
        return False
    
    crear_backup(package_path)
    
    try:
        with open(package_path, 'r', encoding='utf-8') as f:
            package_data = json.load(f)
        
        # Actualizar script de desarrollo con debugging
        if 'scripts' not in package_data:
            package_data['scripts'] = {}
        
        package_data['scripts']['dev:debug'] = "node --inspect=0.0.0.0:24678 ./node_modules/.bin/vite --host 0.0.0.0 --mode development"
        
        with open(package_path, 'w', encoding='utf-8') as f:
            json.dump(package_data, f, indent=2, ensure_ascii=False)
        
        print(f"✓ {package_path} actualizado con script de debugging")
        return True
        
    except Exception as e:
        print(f"❌ Error actualizando {package_path}: {e}")
        return False


def actualizar_docker_compose():
    """Actualiza docker-compose.debug.yml para exponer puerto de debugging."""
    compose_path = "docker-compose.debug.yml"
    
    if not os.path.exists(compose_path):
        print(f"❌ No se encontro {compose_path}")
        return False
    
    crear_backup(compose_path)
    
    # Leer archivo actual
    try:
        with open(compose_path, 'r', encoding='utf-8') as f:
            contenido = f.read()
        
        # Verificar si ya tiene el puerto de debugging
        if "24678:24678" in contenido:
            print(f"✓ {compose_path} ya tiene configurado el puerto de debugging")
            return True
        
        # Buscar la seccion del frontend para agregar el puerto
        lineas = contenido.split('\n')
        nuevas_lineas = []
        en_frontend = False
        puerto_agregado = False
        
        for linea in lineas:
            nuevas_lineas.append(linea)
            
            # Detectar inicio de seccion frontend
            if 'frontend:' in linea and not linea.strip().startswith('#'):
                en_frontend = True
            
            # Si estamos en frontend y encontramos ports, agregar el puerto de debugging
            if en_frontend and 'ports:' in linea and not puerto_agregado:
                # Encontrar la indentacion
                indentacion = len(linea) - len(linea.lstrip())
                # Buscar el siguiente puerto para mantener la indentacion
                siguiente_linea_idx = lineas.index(linea) + 1
                if siguiente_linea_idx < len(lineas):
                    siguiente_linea = lineas[siguiente_linea_idx]
                    if '- "' in siguiente_linea:
                        puerto_indentacion = len(siguiente_linea) - len(siguiente_linea.lstrip())
                        nuevas_lineas.append(' ' * puerto_indentacion + '- "24678:24678"  # Puerto de debugging Node.js')
                        puerto_agregado = True
        
        # Escribir archivo actualizado
        with open(compose_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(nuevas_lineas))
        
        print(f"✓ {compose_path} actualizado con puerto de debugging")
        return True
        
    except Exception as e:
        print(f"❌ Error actualizando {compose_path}: {e}")
        return False


def actualizar_vite_config():
    """Corrige el archivo vite.config.js si tiene errores de encoding."""
    vite_path = "frontend/vite.config.js"
    
    if not os.path.exists(vite_path):
        print(f"❌ No se encontro {vite_path}")
        return False
    
    crear_backup(vite_path)
    
    try:
        # Leer con diferentes encodings
        contenido = None
        for encoding in ['utf-8', 'latin-1', 'cp1252']:
            try:
                with open(vite_path, 'r', encoding=encoding) as f:
                    contenido = f.read()
                break
            except UnicodeDecodeError:
                continue
        
        if contenido is None:
            print(f"❌ No se pudo leer {vite_path} con ningun encoding")
            return False
        
        # Corregir caracteres problematicos
        contenido_corregido = contenido.replace('Configuracin', 'Configuración')
        
        # Escribir archivo corregido
        with open(vite_path, 'w', encoding='utf-8') as f:
            f.write(contenido_corregido)
        
        print(f"✓ {vite_path} corregido")
        return True
        
    except Exception as e:
        print(f"❌ Error corrigiendo {vite_path}: {e}")
        return False


def main():
    """Funcion principal."""
    print("🔧 INICIANDO CORRECCION COMPLETA DE DEBUGGING...")
    print("=" * 60)
    
    # Verificar que estamos en el directorio correcto
    if not os.path.exists("frontend") or not os.path.exists("docker-compose.debug.yml"):
        print("❌ Error: Este script debe ejecutarse desde el directorio raiz del proyecto (vnm-proyectos)")
        sys.exit(1)
    
    print("\n1. Creando configuraciones de VS Code...")
    if not crear_configuraciones_vscode():
        print("❌ Error creando configuraciones de VS Code")
        sys.exit(1)
    
    print("\n2. Actualizando package.json...")
    if not actualizar_package_json():
        print("❌ Error actualizando package.json")
        sys.exit(1)
    
    print("\n3. Actualizando docker-compose.debug.yml...")
    if not actualizar_docker_compose():
        print("❌ Error actualizando docker-compose")
        sys.exit(1)
    
    print("\n4. Corrigiendo vite.config.js...")
    if not actualizar_vite_config():
        print("❌ Error corrigiendo vite.config.js")
        sys.exit(1)
    
    print("\n" + "=" * 60)
    print("✅ CORRECCION COMPLETA FINALIZADA!")
    print("\nPASOS SIGUIENTES:")
    print("1. Copiar configuraciones:")
    print("   copy _vscode\\*.* .vscode\\")
    print("   copy frontend\\_vscode\\*.* frontend\\.vscode\\")
    print("2. Reiniciar entorno:")
    print("   python automate\\vnm_automate.py dev-restart")
    print("3. Probar debugging:")
    print("   F5 -> 'FullStack Debug (Complete)'")
    print("\n📝 Archivos de backup creados para restaurar si es necesario.")


if __name__ == "__main__":
    main()