#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VNM Automate - Script Maestro de Automatizacion
===============================================

Script centralizado para ejecutar todos los automatismos del proyecto VNM
desde el directorio raiz sin tener que navegar a subcarpetas.

Funcionalidades disponibles:
- Gestion del entorno de desarrollo (iniciar, detener, diagnosticar)
- Configuracion de VS Code
- Formateo y validacion de codigo
- Backup y restauracion de base de datos
- Testing automatizado

Uso:
    python automate/vnm_automate.py <comando> [opciones]

Comandos disponibles:
    dev-start        Iniciar entorno de desarrollo
    dev-stop         Detener entorno de desarrollo  
    dev-status       Diagnosticar estado del entorno
    dev-restart      Reiniciar entorno completo
    dev-backup       Realizar backup de base de datos
    
    vscode-install   Instalar configuracion VS Code
    vscode-verify    Verificar configuracion VS Code
    
    code-format      Formatear codigo con Black y Flake8
    code-validate    Validar codigo sin formatear
    
    db-recreate      Recrear base de datos desde cero
    db-backup        Backup manual de base de datos
    
    test-all         Ejecutar todos los tests
    test-backend     Ejecutar tests del backend
    test-frontend    Ejecutar tests del frontend

Autor: MiniMax Agent
"""

import sys
import os
import subprocess
import argparse
from pathlib import Path
from typing import List, Optional

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

class VNMAutomate:
    """Clase principal para automatizacion VNM"""
    
    def __init__(self):
        # El script esta en automate/, el root_dir es el directorio padre
        self.root_dir = Path(__file__).parent.parent
        self.automate_dir = self.root_dir / "automate"
        self.devtools_dir = self.root_dir / "devtools"
        
    def _print_color(self, message: str, color: str = Color.WHITE, bold: bool = False):
        """Imprimir mensaje con color"""
        prefix = Color.BOLD if bold else ""
        print(f"{prefix}{color}{message}{Color.END}")
        
    def _print_header(self, title: str):
        """Imprimir encabezado simple"""
        print(f"{title}")
        print("-" * len(title))
        
    def _print_success(self, message: str):
        """Imprimir mensaje de exito"""
        print(f"OK - {message}")
        
    def _print_error(self, message: str):
        """Imprimir mensaje de error"""
        print(f"ERROR - {message}")
        
    def _print_info(self, message: str):
        """Imprimir mensaje informativo"""
        print(f"INFO - {message}")
        
    def _run_script(self, script_path: Path, args: List[str] = None) -> int:
        """Ejecutar script de Python"""
        if not script_path.exists():
            self._print_error(f"Script no encontrado: {script_path}")
            return 1
            
        cmd = [sys.executable, str(script_path)]
        if args:
            cmd.extend(args)
            
        try:
            result = subprocess.run(cmd, cwd=self.root_dir)
            return result.returncode
        except Exception as e:
            self._print_error(f"Error ejecutando {script_path.name}: {e}")
            return 1
    
    # Comandos de desarrollo
    def dev_start(self):
        """Iniciar entorno de desarrollo"""
        self._print_header("INICIANDO ENTORNO DE DESARROLLO")
        return self._run_script(self.devtools_dir / "orquestador_desarrollo.py", ["iniciar"])
    
    def dev_stop(self):
        """Detener entorno de desarrollo"""
        self._print_header("DETENIENDO ENTORNO DE DESARROLLO")
        return self._run_script(self.devtools_dir / "orquestador_desarrollo.py", ["terminar"])
    
    def dev_status(self):
        """Diagnosticar estado del entorno"""
        self._print_header("DIAGNOSTICO DEL ENTORNO")
        return self._run_script(self.devtools_dir / "orquestador_desarrollo.py", ["diagnosticar"])
    
    def dev_restart(self):
        """Reiniciar entorno completo"""
        self._print_header("REINICIANDO ENTORNO COMPLETO")
        return self._run_script(self.devtools_dir / "orquestador_desarrollo.py", ["regenerar"])
    
    def dev_backup(self):
        """Realizar backup de base de datos"""
        self._print_header("BACKUP DE BASE DE DATOS")
        return self._run_script(self.devtools_dir / "orquestador_desarrollo.py", ["backup"])
    
    # Comandos de VS Code
    def vscode_install(self):
        """Instalar configuracion VS Code"""
        self._print_header("INSTALANDO CONFIGURACION VS CODE")
        return self._run_script(self.automate_dir / "instalar_vscode_config.py")
    
    def vscode_verify(self):
        """Verificar configuracion VS Code"""
        self._print_header("VERIFICANDO CONFIGURACION VS CODE")
        return self._run_script(self.automate_dir / "verificar_vscode_instalado.py")
    
    # Comandos de codigo
    def code_format(self):
        """Formatear codigo con Black y Flake8"""
        self._print_header("FORMATEANDO CODIGO")
        return self._run_script(self.automate_dir / "formatear_codigo.py")
    
    def code_validate(self):
        """Validar codigo sin formatear"""
        self._print_header("VALIDANDO CODIGO")
        return self._run_script(self.automate_dir / "validar_configuracion_vscode.py")
    
    # Comandos de base de datos
    def db_recreate(self):
        """Recrear base de datos desde cero"""
        self._print_header("RECREANDO BASE DE DATOS")
        return self._run_script(self.automate_dir / "recrear_base_datos.py")
    
    def db_backup(self):
        """Backup manual de base de datos"""
        self._print_header("BACKUP MANUAL DE BASE DE DATOS")
        return self.dev_backup()
    
    # Comandos de testing
    def test_all(self):
        """Ejecutar todos los tests"""
        self._print_header("EJECUTANDO TODOS LOS TESTS")
        # Ejecutar tests de backend
        backend_result = self._run_script(self.automate_dir / "test-black-formatting.py")
        # TODO: Agregar tests de frontend cuando esten disponibles
        return backend_result
    
    def test_backend(self):
        """Ejecutar tests del backend"""
        self._print_header("EJECUTANDO TESTS DEL BACKEND")
        return self._run_script(self.automate_dir / "test-black-formatting.py")
    
    def test_frontend(self):
        """Ejecutar tests del frontend"""
        self._print_header("EJECUTANDO TESTS DEL FRONTEND")
        self._print_info("Tests de frontend pendientes de implementacion")
        return 0
    
    def show_help(self):
        """Mostrar ayuda"""
        self._print_header("VNM AUTOMATE - COMANDOS DISPONIBLES")
        
        commands = {
            "DESARROLLO": [
                ("dev-start", "Iniciar entorno de desarrollo"),
                ("dev-stop", "Detener entorno de desarrollo"),
                ("dev-status", "Diagnosticar estado del entorno"),
                ("dev-restart", "Reiniciar entorno completo"),
                ("dev-backup", "Realizar backup de base de datos"),
            ],
            "VS CODE": [
                ("vscode-install", "Instalar configuracion VS Code"),
                ("vscode-verify", "Verificar configuracion VS Code"),
            ],
            "CODIGO": [
                ("code-format", "Formatear codigo con Black y Flake8"),
                ("code-validate", "Validar codigo sin formatear"),
            ],
            "BASE DE DATOS": [
                ("db-recreate", "Recrear base de datos desde cero"),
                ("db-backup", "Backup manual de base de datos"),
            ],
            "TESTING": [
                ("test-all", "Ejecutar todos los tests"),
                ("test-backend", "Ejecutar tests del backend"),
                ("test-frontend", "Ejecutar tests del frontend"),
            ]
        }
        
        for category, cmd_list in commands.items():
            print(f"\n{category}:")
            for cmd, desc in cmd_list:
                print(f"  {cmd:<20} {desc}")
        
        print("\nUso:")
        print("  python automate/vnm_automate.py <comando>")
        print("\nEjemplos:")
        print("  python automate/vnm_automate.py dev-start")
        print("  python automate/vnm_automate.py vscode-install")
        print("  python automate/vnm_automate.py code-format")

def main():
    """Funcion principal"""
    automate = VNMAutomate()
    
    if len(sys.argv) < 2:
        automate.show_help()
        return 1
    
    command = sys.argv[1].lower()
    
    # Mapeo de comandos a metodos
    command_map = {
        # Desarrollo
        'dev-start': automate.dev_start,
        'dev-stop': automate.dev_stop,
        'dev-status': automate.dev_status,
        'dev-restart': automate.dev_restart,
        'dev-backup': automate.dev_backup,
        
        # VS Code
        'vscode-install': automate.vscode_install,
        'vscode-verify': automate.vscode_verify,
        
        # Codigo
        'code-format': automate.code_format,
        'code-validate': automate.code_validate,
        
        # Base de datos
        'db-recreate': automate.db_recreate,
        'db-backup': automate.db_backup,
        
        # Testing
        'test-all': automate.test_all,
        'test-backend': automate.test_backend,
        'test-frontend': automate.test_frontend,
        
        # Ayuda
        'help': automate.show_help,
        '--help': automate.show_help,
        '-h': automate.show_help,
    }
    
    if command in command_map:
        try:
            return command_map[command]()
        except KeyboardInterrupt:
            automate._print_error("Operacion cancelada por el usuario")
            return 1
        except Exception as e:
            automate._print_error(f"Error inesperado: {e}")
            return 1
    else:
        automate._print_error(f"Comando desconocido: {command}")
        automate.show_help()
        return 1

if __name__ == "__main__":
    exit(main())