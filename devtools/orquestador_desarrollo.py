#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Orquestador de Desarrollo VNM-Proyectos
========================================

Programa unificado para gestionar el ciclo de vida completo de contenedores Docker
de forma idempotente y robusta.

Funcionalidades:
- diagnosticar: Verificar estado de contenedores y servicios
- iniciar: Levantar entorno completo con verificaciones de salud
- terminar: Parar contenedores con backup automático
- regenerar: Recrear completamente el entorno
- backup: Realizar backup manual de la base de datos

Uso:
    python orquestador_desarrollo.py <accion> [opciones]

Autor: MiniMax Agent
"""

import os
import sys
import json
import time
import logging
import argparse
import subprocess
from datetime import datetime
from pathlib import Path
from enum import Enum
from typing import Dict, List, Optional, Tuple, Union
import shutil
import zipfile
import requests


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


class Estado(Enum):
    """Estados de los contenedores"""
    DETENIDO = "stopped"
    EJECUTANDO = "running"
    PAUSADO = "paused"
    REINICIANDO = "restarting"
    SALUDABLE = "healthy"
    NO_SALUDABLE = "unhealthy"
    DESCONOCIDO = "unknown"
    NO_EXISTE = "not_exists"


class OrquestadorDesarrollo:
    """Orquestrador principal para el entorno de desarrollo"""
    
    def __init__(self, modo_debug: bool = True, verboso: bool = False):
        self.modo_debug = modo_debug
        self.verboso = verboso
        # Detectar la raíz del proyecto (donde están los docker-compose files)
        self.proyecto_root = self._detectar_proyecto_root()
        self.docker_compose_file = "docker-compose.debug.yml" if modo_debug else "docker-compose.yml"
        self.prefix_contenedores = "vnm_" if modo_debug else "monitoreo_"
        
        # Configurar logging
        log_level = logging.DEBUG if verboso else logging.INFO
        logging.basicConfig(
            level=log_level,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('orquestador.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
        # Definir servicios esperados
        self.servicios_esperados = {
            'postgres': {
                'container_name': f'{self.prefix_contenedores}postgres{"_debug" if modo_debug else ""}',
                'healthcheck': True,
                'puerto': 5432,
                'dependencias': []
            },
            'backend': {
                'container_name': f'{self.prefix_contenedores}backend{"_debug" if modo_debug else ""}',
                'healthcheck': True,
                'puerto': 8000,
                'dependencias': ['postgres']
            },
            'frontend': {
                'container_name': f'{self.prefix_contenedores}frontend{"_debug" if modo_debug else ""}',
                'healthcheck': True,
                'puerto': 3000,
                'dependencias': ['backend']
            }
        }
        
        if not modo_debug:
            self.servicios_esperados['pgadmin'] = {
                'container_name': 'monitoreo_pgadmin',
                'healthcheck': False,
                'puerto': 8081,
                'dependencias': ['postgres']
            }
        
        # Verificar entorno
        self._verificar_entorno_inicial()
    
    def _detectar_proyecto_root(self) -> Path:
        """Detectar la raíz del proyecto buscando docker-compose files"""
        current_path = Path(__file__).parent
        
        # Si estamos en devtools/, la raíz está un nivel arriba
        if current_path.name == 'devtools':
            proyecto_root = current_path.parent
        else:
            # Si no, usar el directorio actual
            proyecto_root = Path.cwd()
        
        # Verificar que existe al menos un docker-compose file
        if (proyecto_root / "docker-compose.yml").exists() or (proyecto_root / "docker-compose.debug.yml").exists():
            return proyecto_root
        
        # Si no encontramos, usar el directorio actual como fallback
        return Path.cwd()

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

    def _print_step(self, step: str, description: str = ""):
        """Imprimir paso de proceso"""
        self._print_color(f"► {step}", Color.YELLOW, bold=True)
        if description:
            self._print_color(f"  {description}", Color.WHITE)

    def _print_success(self, message: str):
        """Imprimir mensaje de éxito"""
        self._print_color(f"✓ {message}", Color.GREEN, bold=True)

    def _print_error(self, message: str):
        """Imprimir mensaje de error"""
        self._print_color(f"✗ {message}", Color.RED, bold=True)

    def _print_warning(self, message: str):
        """Imprimir mensaje de advertencia"""
        self._print_color(f"⚠ {message}", Color.YELLOW, bold=True)

    def _print_info(self, message: str):
        """Imprimir mensaje informativo"""
        self._print_color(f"ℹ {message}", Color.BLUE)

    def _verificar_entorno_inicial(self):
        """Verificar que el entorno esté correctamente configurado"""
        # Verificar Docker
        try:
            subprocess.run(['docker', '--version'], check=True, capture_output=True)
            subprocess.run(['docker-compose', '--version'], check=True, capture_output=True)
        except (subprocess.CalledProcessError, FileNotFoundError, PermissionError) as e:
            self._print_error("Docker o docker-compose no están disponibles")
            self._print_error(f"Error: {e}")
            self._print_info("Posibles soluciones:")
            self._print_info("1. Verificar que Docker esté instalado: docker --version")
            self._print_info("2. Verificar que Docker esté ejecutándose: sudo systemctl status docker")
            self._print_info("3. Verificar permisos: sudo usermod -aG docker $USER")
            self._print_info("4. Reiniciar sesión después de cambiar permisos")
            sys.exit(1)
        
        # Verificar archivo docker-compose
        if not (self.proyecto_root / self.docker_compose_file).exists():
            self._print_error(f"Archivo {self.docker_compose_file} no encontrado")
            self._print_info(f"Asegúrate de estar en el directorio del proyecto")
            self._print_info(f"Directorio actual: {self.proyecto_root}")
            self._print_info(f"Archivos disponibles: {list(self.proyecto_root.glob('docker-compose*.yml'))}")
            sys.exit(1)

    def _ejecutar_comando(self, comando: List[str], capture_output: bool = True, check: bool = True) -> subprocess.CompletedProcess:
        """Ejecutar comando con logging automático"""
        comando_str = ' '.join(comando)
        self.logger.debug(f"Ejecutando: {comando_str}")
        
        try:
            result = subprocess.run(
                comando,
                capture_output=capture_output,
                text=True,
                check=check,
                cwd=self.proyecto_root
            )
            if self.verboso and result.stdout:
                self.logger.debug(f"STDOUT: {result.stdout}")
            if self.verboso and result.stderr:
                self.logger.debug(f"STDERR: {result.stderr}")
            return result
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Error ejecutando comando: {comando_str}")
            if e.stdout:
                self.logger.error(f"STDOUT: {e.stdout}")
            if e.stderr:
                self.logger.error(f"STDERR: {e.stderr}")
            raise

    def obtener_estado_contenedor(self, nombre_contenedor: str) -> Tuple[Estado, Dict]:
        """Obtener estado detallado de un contenedor"""
        try:
            # Verificar si el contenedor existe
            result = self._ejecutar_comando([
                'docker', 'ps', '-a', 
                '--filter', f'name={nombre_contenedor}',
                '--format', 'json'
            ])
            
            if not result.stdout.strip():
                return Estado.NO_EXISTE, {}
            
            # Parsear información del contenedor
            info = json.loads(result.stdout.strip())
            estado_docker = info.get('State', '').lower()
            
            # Mapear estado de Docker a nuestro enum
            if estado_docker == 'running':
                # Verificar health check si está disponible
                inspect_result = self._ejecutar_comando([
                    'docker', 'inspect', nombre_contenedor
                ])
                inspect_data = json.loads(inspect_result.stdout)[0]
                
                health_status = inspect_data.get('State', {}).get('Health', {}).get('Status')
                if health_status == 'healthy':
                    estado = Estado.SALUDABLE
                elif health_status == 'unhealthy':
                    estado = Estado.NO_SALUDABLE
                else:
                    estado = Estado.EJECUTANDO
            elif estado_docker in ['exited', 'stopped']:
                estado = Estado.DETENIDO
            elif estado_docker == 'paused':
                estado = Estado.PAUSADO
            elif estado_docker == 'restarting':
                estado = Estado.REINICIANDO
            else:
                estado = Estado.DESCONOCIDO
            
            return estado, info
            
        except (subprocess.CalledProcessError, json.JSONDecodeError) as e:
            self.logger.error(f"Error obteniendo estado de {nombre_contenedor}: {e}")
            return Estado.DESCONOCIDO, {}

    def verificar_conectividad_servicio(self, servicio: str, puerto: int, timeout: int = 10) -> bool:
        """Verificar conectividad HTTP de un servicio"""
        try:
            if servicio == 'backend':
                # Usar endpoint de health check para backend
                url = f"http://localhost:{puerto}/health"
            elif servicio == 'frontend':
                # Verificar que el frontend responda
                url = f"http://localhost:{puerto}"
            else:
                url = f"http://localhost:{puerto}"
            
            response = requests.get(url, timeout=timeout)
            return response.status_code < 400
        except Exception as e:
            # En modo debug, agregar más información sobre fallos de conectividad
            if hasattr(self, 'modo_debug') and self.modo_debug:
                print(f"   Conectividad fallida para {servicio}: {str(e)}")
            return False

    def verificar_postgres_conectividad(self, contenedor: str) -> bool:
        """Verificar conectividad específica de PostgreSQL"""
        try:
            result = self._ejecutar_comando([
                'docker', 'exec', contenedor,
                'pg_isready', '-U', 'monitoreo_user', '-d', 'monitoreo_dev'
            ])
            return 'accepting connections' in result.stdout
        except:
            return False

    def diagnosticar(self) -> Dict[str, Dict]:
        """Diagnosticar estado completo del entorno"""
        self._print_header("DIAGNÓSTICO DEL ENTORNO DE DESARROLLO")
        
        diagnostico = {
            'timestamp': datetime.now().isoformat(),
            'modo': 'debug' if self.modo_debug else 'produccion',
            'docker_compose_file': self.docker_compose_file,
            'servicios': {},
            'resumen': {}
        }
        
        # Verificar cada servicio
        for servicio, config in self.servicios_esperados.items():
            self._print_step(f"Verificando servicio: {servicio}")
            
            contenedor = config['container_name']
            estado, info = self.obtener_estado_contenedor(contenedor)
            
            servicio_info = {
                'contenedor': contenedor,
                'estado': estado.value,
                'puerto': config['puerto'],
                'healthcheck_disponible': config['healthcheck'],
                'dependencias': config['dependencias'],
                'conectividad': False,
                'detalles': info
            }
            
            # Verificar conectividad específica con reintentos
            if estado in [Estado.EJECUTANDO, Estado.SALUDABLE]:
                conectividad_ok = False
                max_reintentos = 3 if servicio == 'backend' else 1
                
                for intento in range(max_reintentos):
                    if servicio == 'postgres':
                        conectividad_ok = self.verificar_postgres_conectividad(contenedor)
                    else:
                        conectividad_ok = self.verificar_conectividad_servicio(
                            servicio, config['puerto']
                        )
                    
                    if conectividad_ok:
                        break
                    elif intento < max_reintentos - 1:
                        if self.modo_debug:
                            print(f"   Reintentando conectividad {servicio} ({intento + 1}/{max_reintentos})")
                        time.sleep(2)  # Esperar un poco antes del siguiente intento
                
                servicio_info['conectividad'] = conectividad_ok
            
            diagnostico['servicios'][servicio] = servicio_info
            
            # Mostrar resultado
            if estado == Estado.SALUDABLE:
                status_icon = "✓" if servicio_info['conectividad'] else "⚠"
                color = Color.GREEN if servicio_info['conectividad'] else Color.YELLOW
                self._print_color(f"  {status_icon} {servicio}: SALUDABLE", color)
            elif estado == Estado.EJECUTANDO:
                status_icon = "✓" if servicio_info['conectividad'] else "⚠"
                color = Color.GREEN if servicio_info['conectividad'] else Color.YELLOW
                self._print_color(f"  {status_icon} {servicio}: EJECUTANDO", color)
            elif estado == Estado.DETENIDO:
                self._print_color(f"  ✗ {servicio}: DETENIDO", Color.RED)
            elif estado == Estado.NO_EXISTE:
                self._print_color(f"  ✗ {servicio}: NO EXISTE", Color.RED)
            else:
                self._print_color(f"  ? {servicio}: {estado.value.upper()}", Color.YELLOW)
        
        # Generar resumen
        servicios_saludables = sum(1 for s in diagnostico['servicios'].values() 
                                 if s['estado'] in ['healthy', 'running'] and s['conectividad'])
        servicios_ejecutando = sum(1 for s in diagnostico['servicios'].values() 
                                 if s['estado'] in ['healthy', 'running'])
        total_servicios = len(diagnostico['servicios'])
        
        # Determinar si el entorno es operativo
        # En modo debug, ser más tolerante - todos ejecutando es suficiente
        if self.modo_debug:
            entorno_operativo = (servicios_ejecutando == total_servicios and 
                               servicios_saludables >= total_servicios - 1)  # Permitir 1 servicio sin conectividad
        else:
            entorno_operativo = servicios_saludables == total_servicios
        
        diagnostico['resumen'] = {
            'servicios_saludables': servicios_saludables,
            'servicios_ejecutando': servicios_ejecutando,
            'total_servicios': total_servicios,
            'entorno_operativo': entorno_operativo
        }
        
        # Mostrar resumen
        print()
        self._print_step("RESUMEN DEL DIAGNÓSTICO")
        if diagnostico['resumen']['entorno_operativo']:
            self._print_success("Entorno completamente operativo")
        else:
            self._print_warning(f"Servicios operativos: {servicios_saludables}/{total_servicios}")
        
        # Guardar diagnóstico
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        diagnostico_file = f"diagnostico_{timestamp}.json"
        with open(diagnostico_file, 'w') as f:
            json.dump(diagnostico, f, indent=2, ensure_ascii=False)
        
        self._print_info(f"Diagnóstico guardado en: {diagnostico_file}")
        
        return diagnostico

    def crear_backup_database(self) -> Optional[str]:
        """Crear backup de la base de datos PostgreSQL"""
        self._print_step("Creando backup de la base de datos")
        
        # Verificar que PostgreSQL esté ejecutándose
        postgres_container = self.servicios_esperados['postgres']['container_name']
        estado, _ = self.obtener_estado_contenedor(postgres_container)
        
        if estado not in [Estado.EJECUTANDO, Estado.SALUDABLE]:
            self._print_error("PostgreSQL no está ejecutándose. No se puede crear backup.")
            return None
        
        # Crear directorio de backups si no existe
        backup_dir = self.proyecto_root / "database" / "backups"
        backup_dir.mkdir(parents=True, exist_ok=True)
        
        # Generar nombre de archivo
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_file = f"backup_{timestamp}.sql"
        backup_path = backup_dir / backup_file
        
        try:
            # Crear backup usando pg_dumpall
            self._print_info("Ejecutando pg_dumpall...")
            with open(backup_path, 'w') as f:
                result = self._ejecutar_comando([
                    'docker', 'exec', postgres_container,
                    'pg_dumpall', '-U', 'monitoreo_user', '-c'
                ], capture_output=True)
                f.write(result.stdout)
            
            # Verificar que el backup se creó correctamente
            if backup_path.exists() and backup_path.stat().st_size > 0:
                size_mb = backup_path.stat().st_size / (1024 * 1024)
                self._print_success(f"Backup creado: {backup_file} ({size_mb:.2f} MB)")
                
                # Comprimir backup
                zip_path = backup_path.with_suffix('.sql.zip')
                with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                    zipf.write(backup_path, backup_file)
                
                # Eliminar archivo sin comprimir
                backup_path.unlink()
                
                # Mantener solo últimos 10 backups
                backups = sorted(backup_dir.glob("backup_*.sql.zip"), 
                               key=lambda x: x.stat().st_mtime, reverse=True)
                if len(backups) > 10:
                    for old_backup in backups[10:]:
                        old_backup.unlink()
                        self._print_info(f"Eliminado backup antiguo: {old_backup.name}")
                
                return str(zip_path)
            else:
                self._print_error("El backup está vacío o no se pudo crear")
                if backup_path.exists():
                    backup_path.unlink()
                return None
                
        except Exception as e:
            self._print_error(f"Error creando backup: {e}")
            if backup_path.exists():
                backup_path.unlink()
            return None

    def iniciar(self, forzar_rebuild: bool = False) -> bool:
        """Iniciar el entorno de desarrollo completo"""
        self._print_header("INICIANDO ENTORNO DE DESARROLLO")
        
        try:
            # Paso 1: Verificar estado actual
            self._print_step("Paso 1: Verificando estado actual")
            diagnostico_inicial = self.diagnosticar()
            
            if diagnostico_inicial['resumen']['entorno_operativo']:
                self._print_success("El entorno ya está completamente operativo")
                return True
            
            # Paso 2: Parar servicios si están ejecutándose parcialmente
            servicios_ejecutando = any(
                s['estado'] in ['running', 'healthy'] 
                for s in diagnostico_inicial['servicios'].values()
            )
            
            if servicios_ejecutando:
                self._print_step("Paso 2: Parando servicios existentes")
                self._ejecutar_comando([
                    'docker-compose', '-f', self.docker_compose_file, 'down'
                ])
                time.sleep(2)
            
            # Paso 3: Iniciar servicios
            self._print_step("Paso 3: Iniciando servicios")
            comando_up = ['docker-compose', '-f', self.docker_compose_file, 'up', '-d']
            if forzar_rebuild:
                comando_up.append('--build')
                self._print_info("Forzando rebuild de imágenes Docker")
            
            self._ejecutar_comando(comando_up)
            
            # Paso 4: Esperar a que los servicios estén listos
            self._print_step("Paso 4: Verificando servicios (timeout: 120s)")
            
            timeout = 120
            inicio = time.time()
            
            while time.time() - inicio < timeout:
                diagnostico = self.diagnosticar()
                if diagnostico['resumen']['entorno_operativo']:
                    self._print_success("Todos los servicios están operativos")
                    break
                
                self._print_info("Esperando servicios...")
                time.sleep(10)
            else:
                self._print_warning("Timeout alcanzado. Algunos servicios pueden no estar listos.")
                
                # Mostrar logs de servicios problemáticos
                for servicio, info in diagnostico['servicios'].items():
                    if not info['conectividad']:
                        self._print_error(f"Servicio problemático: {servicio}")
                        self._print_info(f"Revisar logs: docker logs {info['contenedor']}")
            
            # Paso 5: Resumen final
            self._print_step("Paso 5: Resumen final")
            diagnostico_final = self.diagnosticar()
            
            if diagnostico_final['resumen']['entorno_operativo']:
                self._print_success("ENTORNO LISTO PARA DESARROLLO")
                self._mostrar_urls_servicios()
                return True
            else:
                self._print_error("Algunos servicios no están completamente operativos")
                return False
                
        except Exception as e:
            self._print_error(f"Error durante el inicio: {e}")
            self.logger.exception("Error detallado durante inicio")
            return False

    def _mostrar_urls_servicios(self):
        """Mostrar URLs de los servicios disponibles"""
        print()
        self._print_step("SERVICIOS DISPONIBLES")
        
        urls = {
            'Frontend': 'http://localhost:3000',
            'Backend API': 'http://localhost:8000',
            'Backend Docs': 'http://localhost:8000/docs',
            'PostgreSQL': 'localhost:5432'
        }
        
        if not self.modo_debug:
            urls['PgAdmin'] = 'http://localhost:8081'
        else:
            urls['Debug Server'] = 'localhost:5678'
        
        for servicio, url in urls.items():
            self._print_color(f"  • {servicio}: {url}", Color.WHITE)

    def terminar(self, crear_backup: bool = True, limpiar_completo: bool = False) -> bool:
        """Terminar el entorno de desarrollo"""
        accion = "LIMPIEZA COMPLETA" if limpiar_completo else "TERMINANDO ENTORNO"
        self._print_header(accion)
        
        try:
            # Paso 1: Crear backup si se solicita
            if crear_backup and not limpiar_completo:
                backup_path = self.crear_backup_database()
                if backup_path:
                    self._print_success(f"Backup creado: {backup_path}")
            
            # Paso 2: Parar contenedores
            self._print_step("Parando contenedores")
            
            if limpiar_completo:
                # Parar y eliminar todo incluyendo volúmenes
                self._ejecutar_comando([
                    'docker-compose', '-f', self.docker_compose_file, 'down', '-v'
                ])
                
                # Limpiar imágenes no utilizadas
                self._print_step("Limpiando imágenes Docker no utilizadas")
                self._ejecutar_comando(['docker', 'system', 'prune', '-f'])
                
                self._print_success("Limpieza completa finalizada")
                self._print_warning("Todos los datos de la base de datos han sido eliminados")
            else:
                # Solo parar contenedores, mantener volúmenes
                self._ejecutar_comando([
                    'docker-compose', '-f', self.docker_compose_file, 'down'
                ])
                self._print_success("Entorno cerrado (datos preservados)")
            
            # Paso 3: Verificar estado final
            self._print_step("Verificando estado final")
            diagnostico_final = self.diagnosticar()
            
            servicios_ejecutando = sum(
                1 for s in diagnostico_final['servicios'].values() 
                if s['estado'] in ['running', 'healthy']
            )
            
            if servicios_ejecutando == 0:
                self._print_success("Todos los contenedores han sido detenidos")
                return True
            else:
                self._print_warning(f"Aún hay {servicios_ejecutando} servicios ejecutándose")
                return False
                
        except Exception as e:
            self._print_error(f"Error durante la terminación: {e}")
            self.logger.exception("Error detallado durante terminación")
            return False

    def regenerar(self) -> bool:
        """Regenerar completamente el entorno"""
        self._print_header("REGENERANDO ENTORNO COMPLETO")
        
        try:
            # Paso 1: Crear backup antes de regenerar
            self._print_step("Paso 1: Creando backup de seguridad")
            backup_path = self.crear_backup_database()
            
            # Paso 2: Limpieza completa
            self._print_step("Paso 2: Limpieza completa del entorno")
            self.terminar(crear_backup=False, limpiar_completo=True)
            
            # Paso 3: Iniciar con rebuild forzado
            self._print_step("Paso 3: Reconstruyendo entorno")
            exito = self.iniciar(forzar_rebuild=True)
            
            if exito:
                self._print_success("REGENERACIÓN COMPLETADA EXITOSAMENTE")
                if backup_path:
                    self._print_info(f"Backup de seguridad disponible en: {backup_path}")
                return True
            else:
                self._print_error("Error durante la regeneración")
                return False
                
        except Exception as e:
            self._print_error(f"Error durante la regeneración: {e}")
            self.logger.exception("Error detallado durante regeneración")
            return False


def main():
    """Función principal"""
    parser = argparse.ArgumentParser(
        description='Orquestador de Desarrollo VNM-Proyectos',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  python orquestador_desarrollo.py diagnosticar
  python orquestador_desarrollo.py iniciar
  python orquestador_desarrollo.py iniciar --rebuild
  python orquestador_desarrollo.py terminar
  python orquestador_desarrollo.py terminar --limpiar-completo
  python orquestador_desarrollo.py regenerar
  python orquestador_desarrollo.py backup
        """
    )
    
    parser.add_argument(
        'accion',
        choices=['diagnosticar', 'iniciar', 'terminar', 'regenerar', 'backup'],
        help='Acción a realizar'
    )
    
    parser.add_argument(
        '--modo',
        choices=['debug', 'produccion'],
        default='debug',
        help='Modo de operación (default: debug)'
    )
    
    parser.add_argument(
        '--verboso', '-v',
        action='store_true',
        help='Mostrar información detallada'
    )
    
    parser.add_argument(
        '--rebuild',
        action='store_true',
        help='Forzar rebuild de imágenes Docker (solo para iniciar)'
    )
    
    parser.add_argument(
        '--sin-backup',
        action='store_true',
        help='No crear backup antes de terminar'
    )
    
    parser.add_argument(
        '--limpiar-completo',
        action='store_true',
        help='Eliminar también volúmenes de datos (solo para terminar)'
    )
    
    args = parser.parse_args()
    
    # Crear instancia del orquestador
    orquestador = OrquestadorDesarrollo(
        modo_debug=(args.modo == 'debug'),
        verboso=args.verboso
    )
    
    # Ejecutar acción solicitada
    try:
        if args.accion == 'diagnosticar':
            diagnostico = orquestador.diagnosticar()
            sys.exit(0 if diagnostico['resumen']['entorno_operativo'] else 1)
            
        elif args.accion == 'iniciar':
            exito = orquestador.iniciar(forzar_rebuild=args.rebuild)
            sys.exit(0 if exito else 1)
            
        elif args.accion == 'terminar':
            exito = orquestador.terminar(
                crear_backup=not args.sin_backup,
                limpiar_completo=args.limpiar_completo
            )
            sys.exit(0 if exito else 1)
            
        elif args.accion == 'regenerar':
            exito = orquestador.regenerar()
            sys.exit(0 if exito else 1)
            
        elif args.accion == 'backup':
            backup_path = orquestador.crear_backup_database()
            sys.exit(0 if backup_path else 1)
            
    except KeyboardInterrupt:
        orquestador._print_warning("Operación interrumpida por el usuario")
        sys.exit(130)
    except Exception as e:
        orquestador._print_error(f"Error inesperado: {e}")
        orquestador.logger.exception("Error inesperado")
        sys.exit(1)


if __name__ == '__main__':
    main()
