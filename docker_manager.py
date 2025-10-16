#!/usr/bin/env python3
"""
Script simplificado para manejar containers Docker con persistencia
Solo maneja: levantar/bajar containers + base de datos PostgreSQL
"""
import os
import subprocess
import sys
import time


class DockerManager:
    def __init__(self):
        self.project_root = os.path.dirname(os.path.abspath(__file__))
        self.compose_file = "docker-compose.yml"
        self.compose_debug_file = "docker-compose.debug.yml"

    def run_command(self, command, show_output=True):
        """Ejecuta comando y retorna el resultado"""
        try:
            result = subprocess.run(
                command,
                shell=True,
                cwd=self.project_root,
                capture_output=not show_output,
                text=True,
                check=True,
            )
            return True, result.stdout if not show_output else ""
        except subprocess.CalledProcessError as e:
            print(f"ERROR: {e}")
            return False, e.stderr if hasattr(e, "stderr") else str(e)

    def check_docker(self):
        """Verifica si Docker esta disponible"""
        print("Verificando Docker...")
        success, _ = self.run_command("docker --version", False)
        if not success:
            print("ERROR: Docker no esta instalado o no esta en PATH")
            return False

        success, _ = self.run_command("docker-compose --version", False)
        if not success:
            print("ERROR: docker-compose no esta instalado")
            return False

        print("Docker disponible")
        return True

    def start_containers(self, debug_mode=False):
        """Inicia los containers"""
        if not self.check_docker():
            return False

        compose_file = self.compose_debug_file if debug_mode else self.compose_file
        mode_text = "debug" if debug_mode else "produccion"

        print(f"Iniciando containers en modo {mode_text}...")
        print("=" * 50)

        success, _ = self.run_command(f"docker-compose -f {compose_file} up -d")

        if success:
            print("Containers iniciados correctamente")
            self.show_status()
            self.show_urls()
        else:
            print("ERROR: Fallo al iniciar containers")

        return success

    def stop_containers(self, debug_mode=False):
        """Detiene los containers"""
        compose_file = self.compose_debug_file if debug_mode else self.compose_file

        print("Deteniendo containers...")
        success, _ = self.run_command(f"docker-compose -f {compose_file} down")

        if success:
            print("Containers detenidos correctamente")
        else:
            print("ERROR: Fallo al detener containers")

        return success

    def restart_containers(self, debug_mode=False):
        """Reinicia los containers"""
        print("Reiniciando containers...")
        self.stop_containers(debug_mode)
        time.sleep(2)
        return self.start_containers(debug_mode)

    def show_status(self):
        """Muestra estado de los containers"""
        print("\nEstado de containers:")
        print("-" * 30)
        self.run_command("docker-compose ps")

    def show_logs(self, service=None):
        """Muestra logs de los containers"""
        if service:
            print(f"Logs de {service}:")
            self.run_command(f"docker-compose logs -f {service}")
        else:
            print("Logs de todos los servicios:")
            self.run_command("docker-compose logs -f")

    def show_urls(self):
        """Muestra URLs de acceso"""
        print("\nServicios disponibles:")
        print("-" * 30)
        print(" Frontend: http://localhost:3000")
        print(" Backend API: http://localhost:8000")
        print(" Backend Docs: http://localhost:8000/docs")
        print(" pgAdmin: http://localhost:8081")
        print("  - Email: admin@monitoreo.cl")
        print("  - Password: admin123")
        print(" PostgreSQL: localhost:5432")
        print("  - DB: monitoreo_dev")
        print("  - User: monitoreo_user")
        print("  - Password: monitoreo_pass")

    def clean_containers(self):
        """Limpia containers, redes e imagenes no utilizadas"""
        print("Limpiando containers y recursos...")
        self.run_command("docker-compose down -v")
        self.run_command("docker system prune -f")
        print("Limpieza completada")


def main():
    manager = DockerManager()

    if len(sys.argv) < 2:
        print("Uso: python docker_manager.py [comando]")
        print("\nComandos disponibles:")
        print("  start          - Iniciar containers")
        print("  start-debug    - Iniciar containers en modo debug")
        print("  stop           - Detener containers")
        print("  stop-debug     - Detener containers debug")
        print("  restart        - Reiniciar containers")
        print("  restart-debug  - Reiniciar containers debug")
        print("  status         - Ver estado de containers")
        print("  logs [servicio]- Ver logs (opcional: servicio especifico)")
        print("  urls           - Mostrar URLs de acceso")
        print("  clean          - Limpiar containers y recursos")
        sys.exit(1)

    command = sys.argv[1].lower()

    if command == "start":
        manager.start_containers(debug_mode=False)
    elif command == "start-debug":
        manager.start_containers(debug_mode=True)
    elif command == "stop":
        manager.stop_containers(debug_mode=False)
    elif command == "stop-debug":
        manager.stop_containers(debug_mode=True)
    elif command == "restart":
        manager.restart_containers(debug_mode=False)
    elif command == "restart-debug":
        manager.restart_containers(debug_mode=True)
    elif command == "status":
        manager.show_status()
    elif command == "logs":
        service = sys.argv[2] if len(sys.argv) > 2 else None
        manager.show_logs(service)
    elif command == "urls":
        manager.show_urls()
    elif command == "clean":
        manager.clean_containers()
    else:
        print(f"Comando desconocido: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
