#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Setup del Proyecto VNM - Configuracion Inicial
==============================================

Script de configuracion inicial para el proyecto VNM que:
1. Verifica la estructura del proyecto
2. Instala configuracion de VS Code
3. Verifica dependencias
4. Configura automatismos para Windows
5. Prepara el entorno de desarrollo

Uso:
    python setup_proyecto.py

Autor: MiniMax Agent
"""

import sys
import os
import subprocess
import platform
from pathlib import Path

class Color:
    """Colores para output de consola"""
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    END = '\033[0m'

class ProyectoSetup:
    """Clase para configuracion inicial del proyecto"""
    
    def __init__(self):
        self.root_dir = Path(__file__).parent
        self.sistema = platform.system()
        
    def _print_color(self, message: str, color: str = Color.WHITE, bold: bool = False):
        """Imprimir mensaje con color"""
        prefix = Color.BOLD if bold else ""
        print(f"{prefix}{color}{message}{Color.END}")
        
    def _print_header(self, title: str):
        """Imprimir encabezado estilizado"""
        separator = "=" * 60
        self._print_color(separator, Color.CYAN, bold=True)
        self._print_color(f" {title}", Color.CYAN, bold=True)
        self._print_color(separator, Color.CYAN, bold=True)
        
    def _print_step(self, step: str):
        """Imprimir paso de proceso"""
        self._print_color(f">> {step}", Color.YELLOW, bold=True)
        
    def _print_success(self, message: str):
        """Imprimir mensaje de exito"""
        self._print_color(f"[OK] {message}", Color.GREEN, bold=True)
        
    def _print_error(self, message: str):
        """Imprimir mensaje de error"""
        self._print_color(f"[ERROR] {message}", Color.RED, bold=True)
        
    def _print_warning(self, message: str):
        """Imprimir mensaje de advertencia"""
        self._print_color(f"[WARN] {message}", Color.YELLOW)
        
    def _print_info(self, message: str):
        """Imprimir mensaje informativo"""
        self._print_color(f"[INFO] {message}", Color.BLUE)
        
    def verificar_estructura(self) -> bool:
        """Verificar que la estructura del proyecto este correcta"""
        self._print_step("Verificando estructura del proyecto")
        
        directorios_requeridos = [
            "backend",
            "frontend", 
            "database",
            "automate",
            "vscode-config",
            "info"
        ]
        
        archivos_requeridos = [
            "vnm_automate.py",
            "automate/devtools/orquestador_desarrollo.py",
            "automate/instalar_vscode_config.py",
            "vscode-config/launch.json"
        ]
        
        errores = []
        
        # Verificar directorios
        for directorio in directorios_requeridos:
            dir_path = self.root_dir / directorio
            if not dir_path.exists():
                errores.append(f"Directorio faltante: {directorio}")
            else:
                self._print_success(f"Directorio encontrado: {directorio}")
        
        # Verificar archivos
        for archivo in archivos_requeridos:
            file_path = self.root_dir / archivo
            if not file_path.exists():
                errores.append(f"Archivo faltante: {archivo}")
            else:
                self._print_success(f"Archivo encontrado: {archivo}")
        
        if errores:
            self._print_error("Estructura del proyecto incompleta:")
            for error in errores:
                print(f"  - {error}")
            return False
        
        self._print_success("Estructura del proyecto verificada correctamente")
        return True
    
    def verificar_dependencias(self) -> bool:
        """Verificar dependencias del sistema"""
        self._print_step("Verificando dependencias del sistema")
        
        dependencias = [
            ("python", "Python 3.7+"),
            ("docker", "Docker Desktop"),
            ("npm", "Node.js y npm")
        ]
        
        errores = []
        
        for comando, nombre in dependencias:
            try:
                result = subprocess.run([comando, "--version"], 
                                      capture_output=True, text=True, timeout=10)
                if result.returncode == 0:
                    version = result.stdout.strip().split('\\n')[0]
                    self._print_success(f"{nombre}: {version}")
                else:
                    errores.append(f"{nombre} no encontrado o no funciona")
            except (subprocess.TimeoutExpired, FileNotFoundError):
                errores.append(f"{nombre} no encontrado en PATH")
        
        if errores:
            self._print_warning("Dependencias faltantes:")
            for error in errores:
                print(f"  - {error}")
            self._print_info("Puedes continuar, pero algunas funcionalidades pueden no funcionar")
        
        return len(errores) == 0
    
    def instalar_vscode_config(self) -> bool:
        """Instalar configuracion de VS Code"""
        self._print_step("Instalando configuracion de VS Code")
        
        script_path = self.root_dir / "automate" / "instalar_vscode_config.py"
        
        try:
            result = subprocess.run([sys.executable, str(script_path)], 
                                  cwd=self.root_dir, capture_output=True, text=True)
            
            if result.returncode == 0:
                self._print_success("Configuracion de VS Code instalada correctamente")
                return True
            else:
                self._print_error("Error instalando configuracion de VS Code")
                if result.stderr:
                    print(f"Error: {result.stderr}")
                return False
                
        except Exception as e:
            self._print_error(f"Error ejecutando instalador VS Code: {e}")
            return False
    
    def crear_scripts_windows(self) -> bool:
        """Crear scripts especificos para Windows"""
        if self.sistema != "Windows":
            self._print_info("Sistema no Windows, omitiendo scripts especificos")
            return True
            
        self._print_step("Creando scripts especificos para Windows")
        
        # Script para iniciar desarrollo rapido
        batch_content = """@echo off
echo Iniciando entorno de desarrollo VNM...
python vnm_automate.py dev-start
pause
"""
        
        powershell_content = """# Script de inicio rapido VNM
Write-Host "Iniciando entorno de desarrollo VNM..." -ForegroundColor Green
python vnm_automate.py dev-start
Read-Host "Presiona Enter para continuar"
"""
        
        try:
            # Crear script .bat
            with open(self.root_dir / "inicio_rapido.bat", 'w', encoding='utf-8') as f:
                f.write(batch_content)
            
            # Crear script .ps1
            with open(self.root_dir / "inicio_rapido.ps1", 'w', encoding='utf-8') as f:
                f.write(powershell_content)
            
            self._print_success("Scripts de Windows creados")
            return True
            
        except Exception as e:
            self._print_error(f"Error creando scripts Windows: {e}")
            return False
    
    def mostrar_instrucciones_finales(self):
        """Mostrar instrucciones finales de uso"""
        self._print_header("CONFIGURACION COMPLETADA")
        
        self._print_success("El proyecto VNM esta listo para usar")
        
        print(f"\\n{Color.CYAN}{Color.BOLD}PROXIMOS PASOS:{Color.END}")
        
        print(f"\\n{Color.YELLOW}1. Abrir VS Code:{Color.END}")
        print("   code .")
        
        print(f"\\n{Color.YELLOW}2. Instalar extensiones recomendadas:{Color.END}")
        print("   VS Code te preguntara automaticamente")
        
        print(f"\\n{Color.YELLOW}3. Iniciar entorno de desarrollo:{Color.END}")
        print("   python vnm_automate.py dev-start")
        
        if self.sistema == "Windows":
            print("   O simplemente hacer doble clic en: inicio_rapido.bat")
        
        print(f"\\n{Color.YELLOW}4. Debugging en VS Code:{Color.END}")
        print("   Presiona F5 -> Selecciona 'FullStack Debug - Ambos simultaneamente'")
        
        print(f"\\n{Color.CYAN}{Color.BOLD}COMANDOS DISPONIBLES:{Color.END}")
        print("   python vnm_automate.py help    # Ver todos los comandos")
        print("   python vnm_automate.py dev-status    # Ver estado del entorno")
        print("   python vnm_automate.py dev-stop      # Detener entorno")
        
        print(f"\\n{Color.GREEN}{Color.BOLD}El proyecto esta listo para desarrollo!{Color.END}")
    
    def ejecutar_setup(self) -> bool:
        """Ejecutar configuracion completa"""
        self._print_header("SETUP DEL PROYECTO VNM")
        
        self._print_info(f"Sistema detectado: {self.sistema}")
        print()
        
        # Paso 1: Verificar estructura
        if not self.verificar_estructura():
            self._print_error("Setup cancelado por estructura incompleta")
            return False
        
        print()
        
        # Paso 2: Verificar dependencias
        self.verificar_dependencias()
        print()
        
        # Paso 3: Instalar VS Code config
        if not self.instalar_vscode_config():
            self._print_warning("Configuracion VS Code fallo, pero continuando...")
        
        print()
        
        # Paso 4: Scripts Windows
        self.crear_scripts_windows()
        print()
        
        # Paso 5: Instrucciones finales
        self.mostrar_instrucciones_finales()
        
        return True

def main():
    """Funcion principal"""
    try:
        setup = ProyectoSetup()
        success = setup.ejecutar_setup()
        return 0 if success else 1
        
    except KeyboardInterrupt:
        print(f"\\n{Color.YELLOW}Setup cancelado por el usuario{Color.END}")
        return 1
    except Exception as e:
        print(f"\\n{Color.RED}Error inesperado durante setup: {e}{Color.END}")
        return 1

if __name__ == "__main__":
    exit(main())
