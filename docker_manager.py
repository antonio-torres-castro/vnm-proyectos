#!/usr/bin/env python3
"""
Script simplificado para manejar containers Docker
Solo maneja: PostgreSQL + pgAdmin
Frontend y Backend corren localmente
"""
import os
import subprocess
import sys
import time


class DockerManager:
    def __init__(self):
        self.project_root = os.path.dirname(os.path.abspath(__file__))
        self.compose_file = "docker-compose.yml"

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

    def start_containers(self):
        """Inicia los containers de base de datos"""
        if not self.check_docker():
            return False

        print("Iniciando containers de base de datos...")
        print("=" * 50)

        success, _ = self.run_command(f"docker-compose -f {self.compose_file} up -d")

        if success:
            print("Containers iniciados correctamente")
            self.show_status()
            self.show_urls()
        else:
            print("ERROR: Fallo al iniciar containers")

        return success

    def stop_containers(self):
        """Detiene los containers de base de datos"""
        print("Deteniendo containers...")
        success, _ = self.run_command(f"docker-compose -f {self.compose_file} down")

        if success:
            print("Containers detenidos correctamente")
        else:
            print("ERROR: Fallo al detener containers")

        return success

    def restart_containers(self):
        """Reinicia los containers de base de datos"""
        print("Reiniciando containers...")
        self.stop_containers()
        time.sleep(2)
        return self.start_containers()

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
        """Muestra URLs de acceso a la base de datos"""
        print("\nServicios disponibles:")
        print("-" * 30)
        print(" pgAdmin: http://localhost:8081")
        print("  - Email: admin@monitoreo.cl")
        print("  - Password: admin123")
        print(" PostgreSQL: localhost:5432")
        print("  - DB: monitoreo_dev")
        print("  - User: monitoreo_user")
        print("  - Password: monitoreo_pass")
        print("\nPara desarrollo:")
        print(" Frontend: npm run dev (puerto 3000)")
        print(" Backend: uvicorn app.main:app --reload (puerto 8000)")

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
        print("  start          - Iniciar containers de base de datos")
        print("  stop           - Detener containers")
        print("  restart        - Reiniciar containers")
        print("  status         - Ver estado de containers")
        print("  logs [servicio]- Ver logs (opcional: servicio especifico)")
        print("  urls           - Mostrar URLs de acceso")
        print("  clean          - Limpiar containers y recursos")
        sys.exit(1)

    command = sys.argv[1].lower()

    if command == "start":
        manager.start_containers()
    elif command == "stop":
        manager.stop_containers()
    elif command == "restart":
        manager.restart_containers()
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
