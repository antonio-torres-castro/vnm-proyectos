#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verificador de Estructura VNM - Proyecto Reorganizado
====================================================

Script que verifica que la reorganización del proyecto se completó correctamente:
1. Estructura de directorios correcta
2. Automatismos funcionando
3. Configuraciones VS Code instaladas
4. Referencias entre archivos actualizadas

Uso:
    python verificar_estructura.py

Autor: MiniMax Agent
"""

import sys
import os
import json
import subprocess
from pathlib import Path
from typing import List, Dict, Tuple

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

class VerificadorEstructura:
    """Verificador de la nueva estructura del proyecto"""
    
    def __init__(self):
        self.root_dir = Path(__file__).parent
        self.errores = []
        self.warnings = []
        self.exitos = []
        
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
        
    def _success(self, message: str):
        """Registrar éxito"""
        self.exitos.append(message)
        self._print_color(f"✓ {message}", Color.GREEN)
        
    def _error(self, message: str):
        """Registrar error"""
        self.errores.append(message)
        self._print_color(f"✗ {message}", Color.RED, bold=True)
        
    def _warning(self, message: str):
        """Registrar advertencia"""
        self.warnings.append(message)
        self._print_color(f"⚠ {message}", Color.YELLOW)
        
    def verificar_estructura_directorios(self) -> bool:
        """Verificar que los directorios están en su lugar correcto"""
        self._print_color("\\n► Verificando estructura de directorios...", Color.YELLOW, bold=True)
        
        # Directorios principales requeridos
        directorios_requeridos = [
            "backend",
            "frontend", 
            "database",
            "automate",
            "vscode-config",
            "info",
            "logs",
            "mislogs"
        ]
        
        for directorio in directorios_requeridos:
            dir_path = self.root_dir / directorio
            if dir_path.exists() and dir_path.is_dir():
                self._success(f"Directorio '{directorio}' en posición correcta")
            else:
                self._error(f"Directorio '{directorio}' no encontrado")
        
        # Subdirectorios críticos
        subdirectorios_criticos = [
            "automate/devtools",
            "backend/app",
            "frontend/src",
            "database/backups"
        ]
        
        for subdir in subdirectorios_criticos:
            subdir_path = self.root_dir / subdir
            if subdir_path.exists():
                self._success(f"Subdirectorio '{subdir}' presente")
            else:
                self._warning(f"Subdirectorio '{subdir}' no encontrado")
        
        return len(self.errores) == 0
    
    def verificar_archivos_principales(self) -> bool:
        """Verificar archivos principales del proyecto"""
        self._print_color("\\n► Verificando archivos principales...", Color.YELLOW, bold=True)
        
        archivos_principales = [
            ("automate/vnm_automate.py", "Script maestro de automatización"),
            ("setup_proyecto.py", "Script de configuración inicial"),
            ("README.md", "Documentación principal"),
            ("automate/devtools/orquestador_desarrollo.py", "Orquestador de desarrollo"),
            ("automate/instalar_vscode_config.py", "Instalador VS Code"),
            ("vscode-config/launch.json", "Configuración debugging VS Code"),
            (".vscode/launch.json", "Configuración VS Code instalada")
        ]
        
        for archivo, descripcion in archivos_principales:
            file_path = self.root_dir / archivo
            if file_path.exists():
                self._success(f"{descripcion}: {archivo}")
            else:
                if archivo == ".vscode/launch.json":
                    self._warning(f"{descripcion} no instalada: {archivo}")
                else:
                    self._error(f"{descripcion} no encontrado: {archivo}")
        
        return True
    
    def verificar_configuraciones_vscode(self) -> bool:
        """Verificar configuraciones de VS Code"""
        self._print_color("\\n► Verificando configuraciones VS Code...", Color.YELLOW, bold=True)
        
        # Verificar configuración principal
        main_launch = self.root_dir / ".vscode" / "launch.json"
        if main_launch.exists():
            try:
                with open(main_launch, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                
                configs = config.get('configurations', [])
                config_names = [c.get('name') for c in configs]
                
                # Verificar configuraciones específicas
                required_configs = [
                    "FullStack Debug - Ambos simultáneamente",
                    "Backend Debug",
                    "Frontend Debug"
                ]
                
                for req_config in required_configs:
                    if req_config in config_names:
                        self._success(f"Configuración VS Code: {req_config}")
                    else:
                        self._error(f"Configuración VS Code faltante: {req_config}")
                
                # Verificar que todas tienen 'request'
                configs_sin_request = []
                for config_item in configs:
                    if 'request' not in config_item:
                        configs_sin_request.append(config_item.get('name', 'Sin nombre'))
                
                if not configs_sin_request:
                    self._success("Todas las configuraciones tienen atributo 'request' (error solucionado)")
                else:
                    self._error(f"Configuraciones sin 'request': {', '.join(configs_sin_request)}")
                
            except json.JSONDecodeError as e:
                self._error(f"Error en JSON de launch.json: {e}")
            except Exception as e:
                self._error(f"Error leyendo launch.json: {e}")
        else:
            self._warning("Configuración VS Code principal no instalada - ejecuta: python automate/vnm_automate.py vscode-install")
        
        # Verificar configuraciones específicas de proyectos
        project_configs = [
            ("backend/.vscode/launch.json", "Backend"),
            ("frontend/.vscode/launch.json", "Frontend")
        ]
        
        for config_path, project_name in project_configs:
            config_file = self.root_dir / config_path
            if config_file.exists():
                self._success(f"Configuración VS Code {project_name} presente")
            else:
                self._warning(f"Configuración VS Code {project_name} no encontrada")
        
        return True
    
    def verificar_automatismos(self) -> bool:
        """Verificar que los automatismos funcionan"""
        self._print_color("\\n► Verificando automatismos...", Color.YELLOW, bold=True)
        
        # Verificar script maestro
        try:
            result = subprocess.run([sys.executable, "automate/vnm_automate.py", "help"], 
                                  cwd=self.root_dir, capture_output=True, text=True, timeout=30)
            if result.returncode == 0:
                self._success("Script maestro automate/vnm_automate.py funciona correctamente")
            else:
                self._error("Script maestro automate/vnm_automate.py tiene errores")
        except Exception as e:
            self._error(f"Error ejecutando automate/vnm_automate.py: {e}")
        
        # Verificar orquestador
        orquestador_path = self.root_dir / "automate" / "devtools" / "orquestador_desarrollo.py"
        if orquestador_path.exists():
            try:
                result = subprocess.run([sys.executable, str(orquestador_path), "diagnosticar"], 
                                      cwd=self.root_dir, capture_output=True, text=True, timeout=60)
                if "ERROR CRÍTICO" not in result.stdout:
                    self._success("Orquestador de desarrollo accesible")
                else:
                    self._warning("Orquestador accesible pero con problemas de entorno")
            except Exception as e:
                self._warning(f"Orquestador presente pero error en verificación: {e}")
        else:
            self._error("Orquestador de desarrollo no encontrado")
        
        return True
    
    def verificar_referencias_actualizadas(self) -> bool:
        """Verificar que las referencias entre archivos están actualizadas"""
        self._print_color("\\n► Verificando referencias actualizadas...", Color.YELLOW, bold=True)
        
        # Verificar tasks.json de la solución principal
        tasks_file = self.root_dir / ".vscode" / "tasks.json"
        if tasks_file.exists():
            try:
                with open(tasks_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                if "automate/devtools/orquestador_desarrollo.py" in content:
                    self._success("Referencias en tasks.json actualizadas correctamente")
                elif "devtools/orquestador_desarrollo.py" in content:
                    self._error("Referencias en tasks.json NO actualizadas (todavía apuntan a devtools/)")
                else:
                    self._warning("No se encontraron referencias al orquestador en tasks.json")
                    
            except Exception as e:
                self._warning(f"Error verificando tasks.json: {e}")
        
        # Verificar que el orquestador detecta la nueva ubicación
        orquestador_file = self.root_dir / "automate" / "devtools" / "orquestador_desarrollo.py"
        if orquestador_file.exists():
            try:
                with open(orquestador_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                if "current_path.parent.name == 'automate'" in content:
                    self._success("Orquestador actualizado para nueva estructura")
                else:
                    self._warning("Orquestador puede necesitar actualización para nueva estructura")
                    
            except Exception as e:
                self._warning(f"Error verificando orquestador: {e}")
        
        return True
    
    def verificar_documentacion(self) -> bool:
        """Verificar que la documentación está organizada"""
        self._print_color("\\n► Verificando documentación...", Color.YELLOW, bold=True)
        
        info_dir = self.root_dir / "info"
        if info_dir.exists():
            md_files = list(info_dir.glob("*.md"))
            if len(md_files) > 0:
                self._success(f"Documentación organizada en info/ ({len(md_files)} archivos)")
            else:
                self._warning("Carpeta info/ existe pero no contiene documentación")
        else:
            self._error("Carpeta info/ no encontrada")
        
        # Verificar README principal
        readme_main = self.root_dir / "README.md"
        if readme_main.exists():
            try:
                with open(readme_main, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                if "vnm_automate.py" in content and "nueva estructura" in content.lower():
                    self._success("README principal actualizado para nueva estructura")
                else:
                    self._warning("README principal puede necesitar actualización")
            except Exception as e:
                self._warning(f"Error verificando README: {e}")
        
        return True
    
    def mostrar_resumen_final(self):
        """Mostrar resumen final de la verificación"""
        self._print_color("\\n" + "=" * 60, Color.CYAN, bold=True)
        self._print_color(" RESUMEN DE VERIFICACIÓN", Color.CYAN, bold=True)
        self._print_color("=" * 60, Color.CYAN, bold=True)
        
        print(f"\\n{Color.GREEN}{Color.BOLD}✓ ÉXITOS: {len(self.exitos)}{Color.END}")
        if len(self.exitos) > 0:
            for exito in self.exitos[-5:]:  # Mostrar últimos 5
                print(f"  • {exito}")
            if len(self.exitos) > 5:
                print(f"  ... y {len(self.exitos) - 5} más")
        
        if self.warnings:
            print(f"\\n{Color.YELLOW}{Color.BOLD}⚠ ADVERTENCIAS: {len(self.warnings)}{Color.END}")
            for warning in self.warnings:
                print(f"  • {warning}")
        
        if self.errores:
            print(f"\\n{Color.RED}{Color.BOLD}✗ ERRORES: {len(self.errores)}{Color.END}")
            for error in self.errores:
                print(f"  • {error}")
        
        print()
        
        if len(self.errores) == 0:
            if len(self.warnings) == 0:
                self._print_color("🎉 ¡PERFECTO! La reorganización se completó exitosamente", Color.GREEN, bold=True)
                self._print_color("✅ El proyecto está listo para usar con la nueva estructura", Color.GREEN)
            else:
                self._print_color("✅ Reorganización EXITOSA con advertencias menores", Color.GREEN, bold=True)
                self._print_color("🔧 Las advertencias no impiden el funcionamiento normal", Color.YELLOW)
        else:
            self._print_color("❌ Reorganización INCOMPLETA - hay errores críticos", Color.RED, bold=True)
            self._print_color("🔧 Revisa los errores antes de continuar", Color.YELLOW)
        
        print(f"\\n{Color.CYAN}Próximos pasos recomendados:{Color.END}")
        print("1. python setup_proyecto.py        # Configuración inicial")
        print("2. python automate/vnm_automate.py help     # Ver comandos disponibles")
        print("3. python automate/vnm_automate.py dev-start # Iniciar desarrollo")
    
    def ejecutar_verificacion_completa(self):
        """Ejecutar verificación completa"""
        self._print_header("VERIFICADOR DE ESTRUCTURA VNM-PROYECTOS")
        
        self.verificar_estructura_directorios()
        self.verificar_archivos_principales()
        self.verificar_configuraciones_vscode()
        self.verificar_automatismos()
        self.verificar_referencias_actualizadas()
        self.verificar_documentacion()
        
        self.mostrar_resumen_final()
        
        return len(self.errores) == 0

def main():
    """Función principal"""
    try:
        verificador = VerificadorEstructura()
        success = verificador.ejecutar_verificacion_completa()
        return 0 if success else 1
        
    except KeyboardInterrupt:
        print(f"\\n{Color.YELLOW}Verificación cancelada por el usuario{Color.END}")
        return 1
    except Exception as e:
        print(f"\\n{Color.RED}Error inesperado durante verificación: {e}{Color.END}")
        return 1

if __name__ == "__main__":
    exit(main())
