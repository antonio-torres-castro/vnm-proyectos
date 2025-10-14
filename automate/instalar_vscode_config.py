#!/usr/bin/env python3
"""
Instalador de Configuración VS Code - FullStack Debug
Copia automáticamente los archivos de configuración desde vscode-config/ a .vscode/
Autor: MiniMax Agent
"""

import os
import shutil
import json
from pathlib import Path
import platform

def crear_backup_si_existe():
    """Crea backup de la configuración existente si existe"""
    vscode_dir = Path("../.vscode")
    if vscode_dir.exists():
        backup_dir = Path("../.vscode_backup")
        if backup_dir.exists():
            shutil.rmtree(backup_dir)
        shutil.copytree(vscode_dir, backup_dir)
        print(f"✅ Backup creado en: {backup_dir}")
        return True
    return False

def verificar_estructura():
    """Verifica que existe la carpeta vscode-config con los archivos necesarios"""
    # Buscar vscode-config en el directorio padre (vnm-proyectos)
    config_dir = Path("../vscode-config")
    
    if not config_dir.exists():
        print("❌ ERROR: Carpeta 'vscode-config' no encontrada")
        print("   Ubicación esperada: vnm-proyectos/vscode-config/")
        print("   Ejecutando desde: vnm-proyectos/automate/")
        return False
    
    archivos_requeridos = [
        "launch.json",
        "tasks.json", 
        "settings.json",
        "extensions.json"
    ]
    
    archivos_faltantes = []
    for archivo in archivos_requeridos:
        if not (config_dir / archivo).exists():
            archivos_faltantes.append(archivo)
    
    if archivos_faltantes:
        print(f"❌ ERROR: Archivos faltantes en vscode-config/:")
        for archivo in archivos_faltantes:
            print(f"   - {archivo}")
        return False
    
    print("✅ Estructura vscode-config verificada correctamente")
    return True

def instalar_configuracion():
    """Instala la configuración copiando archivos desde vscode-config/ a .vscode/"""
    
    # Buscar vscode-config en el directorio padre
    config_dir = Path("../vscode-config")
    
    # Directorio .vscode en vnm-proyectos (directorio padre)
    vscode_dir = Path("../.vscode")
    
    # Crear directorio .vscode si no existe
    vscode_dir.mkdir(exist_ok=True)
    
    archivos_copiados = []
    errores = []
    
    # Copiar cada archivo
    for archivo_config in config_dir.glob("*.json"):
        archivo_destino = vscode_dir / archivo_config.name
        
        try:
            shutil.copy2(archivo_config, archivo_destino)
            archivos_copiados.append(archivo_config.name)
            print(f"✅ Copiado: {archivo_config.name}")
            
            # Verificar que el JSON es válido
            with open(archivo_destino, 'r', encoding='utf-8') as f:
                json.load(f)
            
        except json.JSONDecodeError as e:
            errores.append(f"❌ Error JSON en {archivo_config.name}: {e}")
        except Exception as e:
            errores.append(f"❌ Error copiando {archivo_config.name}: {e}")
    
    return archivos_copiados, errores

def ajustar_para_windows():
    """Ajusta la configuración específicamente para Windows"""
    sistema = platform.system()
    
    if sistema == "Windows":
        settings_file = Path("../.vscode/settings.json")
        
        if settings_file.exists():
            try:
                with open(settings_file, 'r', encoding='utf-8') as f:
                    settings = json.load(f)
                
                # Ajustar ruta del intérprete de Python para Windows
                if "python.defaultInterpreterPath" in settings:
                    python_path = settings["python.defaultInterpreterPath"]
                    if "/bin/python" in python_path:
                        # Cambiar de Linux a Windows
                        settings["python.defaultInterpreterPath"] = python_path.replace("/bin/python", "\\Scripts\\python.exe")
                        
                        with open(settings_file, 'w', encoding='utf-8') as f:
                            json.dump(settings, f, indent=4)
                        
                        print("✅ Configuración ajustada para Windows")
                
            except Exception as e:
                print(f"⚠️ Warning: No se pudo ajustar configuración para Windows: {e}")

def verificar_instalacion():
    """Verifica que la instalación fue exitosa"""
    vscode_dir = Path("../.vscode")
    
    if not vscode_dir.exists():
        return False, ["Directorio .vscode no fue creado"]
    
    archivos_esperados = ["launch.json", "tasks.json", "settings.json", "extensions.json"]
    errores = []
    
    for archivo in archivos_esperados:
        archivo_path = vscode_dir / archivo
        if not archivo_path.exists():
            errores.append(f"Archivo {archivo} no fue instalado")
        else:
            # Verificar que es JSON válido
            try:
                with open(archivo_path, 'r', encoding='utf-8') as f:
                    json.load(f)
            except json.JSONDecodeError:
                errores.append(f"Archivo {archivo} tiene formato JSON inválido")
    
    return len(errores) == 0, errores

def mostrar_instrucciones_uso():
    """Muestra las instrucciones de uso después de la instalación"""
    print("\n" + "="*60)
    print("🎯 CONFIGURACIÓN INSTALADA - INSTRUCCIONES DE USO")
    print("="*60)
    
    print("\n🔧 Próximos pasos:")
    print("1. Abre VS Code en este directorio")
    print("2. Acepta instalar las extensiones recomendadas")
    print("3. Presiona F5 para debugging")
    print("4. Selecciona: 'FullStack Debug - Ambos simultáneamente'")
    
    print("\n🚀 Configuraciones disponibles:")
    print("• Frontend Debug - Solo React")
    print("• Backend Debug - Solo FastAPI") 
    print("• FullStack Debug - Ambos simultáneamente ⭐")
    print("• FullStack Debug - Compound")
    
    print("\n📋 Requisitos:")
    print("• Docker Desktop ejecutándose")
    print("• Puerto 3000 y 8000 disponibles")
    print("• Extensiones de VS Code instaladas")
    
    print("\n✅ El error 'Attribute request is missing' está solucionado")

def main():
    """Función principal del instalador"""
    print("="*60)
    print("🔧 INSTALADOR DE CONFIGURACIÓN VS CODE - FULLSTACK DEBUG")
    print("="*60)
    print("Autor: MiniMax Agent")
    print(f"Sistema detectado: {platform.system()}")
    print("")
    
    # Verificar estructura
    if not verificar_estructura():
        return 1
    
    # Crear backup si existe configuración previa
    backup_creado = crear_backup_si_existe()
    if backup_creado:
        print("")
    
    # Instalar configuración
    print("🔄 Instalando configuración...")
    archivos_copiados, errores = instalar_configuracion()
    
    if errores:
        print("\n❌ ERRORES durante la instalación:")
        for error in errores:
            print(f"   {error}")
        return 1
    
    # Ajustes específicos para Windows
    ajustar_para_windows()
    
    # Verificar instalación
    print("\n🔍 Verificando instalación...")
    instalacion_ok, errores_verificacion = verificar_instalacion()
    
    if not instalacion_ok:
        print("\n❌ ERRORES en la verificación:")
        for error in errores_verificacion:
            print(f"   {error}")
        return 1
    
    print("\n✅ INSTALACIÓN COMPLETADA EXITOSAMENTE")
    print(f"📁 Archivos instalados: {', '.join(archivos_copiados)}")
    
    mostrar_instrucciones_uso()
    
    return 0

if __name__ == "__main__":
    try:
        exit_code = main()
        exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n⚠️ Instalación cancelada por el usuario")
        exit(1)
    except Exception as e:
        print(f"\n❌ ERROR INESPERADO: {e}")
        exit(1)