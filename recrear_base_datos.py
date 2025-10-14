#!/usr/bin/env python3
"""
Script para recrear completamente la base de datos
Solucion limpia sin parches - solo recreacion completa
"""

import subprocess
import sys
import time

def ejecutar_comando(comando, descripcion):
    """Ejecutar comando y mostrar resultado"""
    print(f"Ejecutando: {descripcion}")
    try:
        resultado = subprocess.run(comando, shell=True, capture_output=True, text=True, check=True)
        if resultado.stdout:
            print(f"  ✓ {descripcion} - OK")
        return True
    except subprocess.CalledProcessError as e:
        print(f"  ✗ Error en {descripcion}")
        print(f"  Error: {e.stderr}")
        return False

def recrear_base_datos():
    """Recrear completamente la base de datos"""
    
    print("RECREACION COMPLETA DE BASE DE DATOS")
    print("=" * 50)
    
    # 1. Detener contenedores
    print("\n1. Deteniendo contenedores...")
    if not ejecutar_comando("docker-compose -f docker-compose.debug.yml down", "Detener contenedores"):
        return False
    
    # 2. Limpieza completa de contenedores e imágenes
    print("\n2. Limpieza completa Docker...")
    ejecutar_comando("docker volume rm vnm-proyectos_postgres_data_debug", "Eliminar volumen postgres")
    ejecutar_comando("docker rmi vnm-proyectos-backend vnm-proyectos-frontend", "Eliminar imágenes para forzar rebuild")
    
    # 3. Levantar solo PostgreSQL
    print("\n3. Levantando PostgreSQL...")
    if not ejecutar_comando("docker-compose -f docker-compose.debug.yml up -d postgres", "Levantar PostgreSQL"):
        return False
    
    # 4. Esperar que PostgreSQL esté listo (los scripts se ejecutan automáticamente)
    print("\n4. Esperando PostgreSQL e inicialización...")
    for i in range(60):
        if ejecutar_comando(
            'docker exec vnm_postgres_debug pg_isready -U monitoreo_user -d monitoreo_dev',
            f"Verificar PostgreSQL (intento {i+1})"
        ):
            # Esperar un poco más para que terminen los scripts de init
            time.sleep(5)
            break
        time.sleep(2)
    else:
        print("  ✗ PostgreSQL no respondió en 120 segundos")
        return False
    
    # 5. Verificar que los scripts de BD se ejecutaron
    print("\n5. Verificando inicialización de BD...")
    if not ejecutar_comando(
        'docker exec vnm_postgres_debug psql -U monitoreo_user -d monitoreo_dev -c "SELECT COUNT(*) FROM seguridad.estados;"',
        "Verificar datos parametría"
    ):
        print("  ⚠ Los scripts de BD pueden no haberse ejecutado completamente")
        print("  PostgreSQL ejecuta scripts en /docker-entrypoint-initdb.d/ automáticamente")
    
    # 6. Reconstruir y levantar backend (forzar rebuild)
    print("\n6. Reconstruyendo y levantando servicios...")
    if not ejecutar_comando("docker-compose -f docker-compose.debug.yml up -d --build", "Reconstruir y levantar servicios"):
        return False
    
    # 7. Esperar que backend esté listo
    print("\n7. Esperando backend...")
    for i in range(30):
        if ejecutar_comando("curl -s http://localhost:8000/health", f"Verificar backend (intento {i+1})"):
            break
        time.sleep(2)
    else:
        print("  ⚠ Backend no respondió, pero puede estar iniciando")
    
    print("\n" + "=" * 50)
    print("✓ RECREACION COMPLETADA")
    print("\nPROXIMOS PASOS:")
    print("1. curl -X POST http://localhost:8000/api/v1/usuarios/crear-admin")
    print("2. Acceder a http://localhost:3000")
    print("3. Login: admin@monitoreo.cl / admin123")
    
    return True

if __name__ == "__main__":
    if recrear_base_datos():
        sys.exit(0)
    else:
        print("\n✗ Error en la recreacion")
        sys.exit(1)
