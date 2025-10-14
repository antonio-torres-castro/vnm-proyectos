#!/usr/bin/env python3
"""
Script para diagnosticar y reparar problemas del backend
Identifica por que el backend no es accesible
"""

import subprocess
import sys
import time

def ejecutar_comando(comando, descripcion, capturar_output=True):
    """Ejecutar comando y mostrar resultado"""
    print(f"Ejecutando: {descripcion}")
    try:
        if capturar_output:
            resultado = subprocess.run(comando, shell=True, capture_output=True, text=True, check=True)
            return True, resultado.stdout, resultado.stderr
        else:
            resultado = subprocess.run(comando, shell=True, check=True)
            return True, "", ""
    except subprocess.CalledProcessError as e:
        return False, e.stdout if hasattr(e, 'stdout') else "", e.stderr if hasattr(e, 'stderr') else str(e)

def diagnosticar_contenedores():
    """Verificar estado de contenedores"""
    print("\n1. DIAGNOSTICO DE CONTENEDORES")
    print("=" * 50)
    
    # Verificar Docker
    exito, stdout, stderr = ejecutar_comando("docker --version", "Verificar Docker")
    if not exito:
        print("❌ Docker no está disponible")
        print("Instala Docker Desktop y asegúrate de que esté corriendo")
        return False
    
    print(f"✅ Docker disponible: {stdout.strip()}")
    
    # Estado de contenedores
    exito, stdout, stderr = ejecutar_comando("docker ps -a --filter name=vnm", "Estado contenedores VNM")
    if exito:
        print("📊 Estado de contenedores:")
        print(stdout)
    
    return True

def diagnosticar_backend():
    """Diagnosticar problemas específicos del backend"""
    print("\n2. DIAGNOSTICO DEL BACKEND")
    print("=" * 50)
    
    # Logs del backend
    print("📋 Logs del contenedor backend:")
    exito, stdout, stderr = ejecutar_comando(
        "docker logs vnm_backend_debug --tail 50", 
        "Obtener logs del backend"
    )
    
    if exito:
        print("--- LOGS DEL BACKEND ---")
        print(stdout)
        if stderr:
            print("--- ERRORES ---")
            print(stderr)
    else:
        print("❌ No se pudieron obtener logs del backend")
        print("Posibles causas:")
        print("- El contenedor no existe")
        print("- El contenedor no se ha iniciado")
        
    # Verificar si el contenedor está corriendo
    exito, stdout, stderr = ejecutar_comando(
        'docker ps --filter name=vnm_backend_debug --format "{{.Status}}"',
        "Estado específico del backend"
    )
    
    if exito and stdout.strip():
        print(f"📊 Estado del backend: {stdout.strip()}")
    else:
        print("❌ El contenedor backend no está corriendo")
        
    return True

def verificar_conectividad():
    """Verificar conectividad a servicios"""
    print("\n3. VERIFICACION DE CONECTIVIDAD")
    print("=" * 50)
    
    # Test PostgreSQL
    exito, stdout, stderr = ejecutar_comando(
        'docker exec vnm_postgres_debug pg_isready -U monitoreo_user -d monitoreo_dev',
        "Conectividad PostgreSQL"
    )
    
    if exito:
        print("✅ PostgreSQL está corriendo y accesible")
    else:
        print("❌ PostgreSQL no está accesible")
        print(f"Error: {stderr}")
        
    # Test Backend API
    exito, stdout, stderr = ejecutar_comando(
        "curl -s -o /dev/null -w '%{http_code}' http://localhost:8000/health",
        "Test API Backend"
    )
    
    if exito and "200" in stdout:
        print("✅ Backend API está respondiendo")
    else:
        print("❌ Backend API no está respondiendo")
        print("Intentando conexión básica...")
        
        # Test básico de puerto
        exito2, stdout2, stderr2 = ejecutar_comando(
            "curl -s --connect-timeout 5 http://localhost:8000",
            "Test conexión puerto 8000"
        )
        
        if not exito2:
            print("❌ Puerto 8000 no está disponible")
            print("El contenedor backend probablemente no está corriendo")

def reconstruir_backend():
    """Reconstruir completamente el backend"""
    print("\n4. RECONSTRUCCION DEL BACKEND")
    print("=" * 50)
    
    respuesta = input("¿Deseas reconstruir completamente el backend? (s/N): ").lower()
    if respuesta != 's':
        print("Reconstrucción cancelada")
        return True
    
    print("🔨 Reconstruyendo backend...")
    
    # Detener backend
    ejecutar_comando("docker-compose -f ../docker-compose.debug.yml stop backend", "Detener backend")
    
    # Eliminar contenedor backend
    ejecutar_comando("docker rm vnm_backend_debug", "Eliminar contenedor backend")
    
    # Eliminar imagen backend
    ejecutar_comando("docker rmi vnm-proyectos-backend", "Eliminar imagen backend")
    
    # Reconstruir y levantar
    exito, stdout, stderr = ejecutar_comando(
        "docker-compose -f ../docker-compose.debug.yml up -d --build backend",
        "Reconstruir y levantar backend"
    )
    
    if exito:
        print("✅ Backend reconstruido")
        print("⏳ Esperando que el backend se inicie...")
        
        # Esperar y verificar
        for i in range(30):
            time.sleep(2)
            exito_test, _, _ = ejecutar_comando(
                "curl -s http://localhost:8000/health",
                f"Test backend (intento {i+1})",
                capturar_output=True
            )
            if exito_test:
                print("✅ Backend está funcionando!")
                return True
                
        print("⚠️ Backend reconstruido pero aún no responde")
        print("Revisa los logs con: docker logs vnm_backend_debug")
    else:
        print("❌ Error reconstruyendo backend")
        print(stderr)
    
    return exito

def main():
    """Función principal de diagnóstico"""
    print("🔧 DIAGNOSTICO Y REPARACION DEL BACKEND")
    print("=" * 60)
    
    # 1. Diagnóstico básico
    if not diagnosticar_contenedores():
        return False
    
    # 2. Diagnóstico específico del backend
    diagnosticar_backend()
    
    # 3. Verificar conectividad
    verificar_conectividad()
    
    # 4. Opción de reconstruir
    reconstruir_backend()
    
    print("\n" + "=" * 60)
    print("🏁 DIAGNOSTICO COMPLETADO")
    print("\nSi el problema persiste:")
    print("1. Revisa logs: docker logs vnm_backend_debug")
    print("2. Verifica Docker Desktop esté corriendo")
    print("3. Intenta recrear toda la BD: python recrear_base_datos.py")
    
    return True

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n❌ Diagnóstico interrumpido por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        sys.exit(1)
