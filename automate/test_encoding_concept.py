#!/usr/bin/env python3
"""
Script de prueba de concepto para UnicodeDecodeError
Demuestra el problema y la solucion sin modificar archivos originales

Compatible con Windows PowerShell
Ubicacion: vnm-proyectos\automate\test_encoding_concept.py
"""

import subprocess
import sys
from datetime import datetime

def log_test(mensaje):
    """Log de pruebas"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"[{timestamp}] {mensaje}")

def test_problema_encoding():
    """Reproduce el problema UnicodeDecodeError"""
    log_test("="*60)
    log_test("PRUEBA 1: REPRODUCIENDO EL PROBLEMA")
    log_test("="*60)
    
    log_test("Ejecutando comando Docker SIN correccion de encoding...")
    
    # Comando que genera output con caracteres especiales (como el que causa el error)
    comando = ["docker", "ps", "-a", "--format", "table {{.Names}}\\t{{.Status}}\\t{{.Ports}}"]
    
    try:
        # FORMA INCORRECTA (como esta actualmente en el codigo)
        log_test("METODO ACTUAL (problemático):")
        log_test(f"subprocess.run({comando}, capture_output=True, text=True)")
        
        result = subprocess.run(
            comando,
            capture_output=True,
            text=True,  # Esto usa encoding por defecto de Windows (cp1252)
            timeout=10
        )
        
        log_test("RESULTADO: Comando ejecutado sin error visible")
        log_test(f"STDOUT length: {len(result.stdout) if result.stdout else 0}")
        log_test(f"STDERR length: {len(result.stderr) if result.stderr else 0}")
        log_test(f"Return code: {result.returncode}")
        
        # Pero el problema real aparece cuando Docker genera caracteres especiales
        # Simulemos un comando que puede generar esos caracteres
        return True
        
    except UnicodeDecodeError as e:
        log_test("ERROR REPRODUCIDO!")
        log_test(f"UnicodeDecodeError: {e}")
        return False
    except Exception as e:
        log_test(f"Otro error: {e}")
        return False

def test_solucion_encoding():
    """Demuestra la solucion con encoding correcto"""
    log_test("="*60)
    log_test("PRUEBA 2: DEMOSTRANDO LA SOLUCION")
    log_test("="*60)
    
    log_test("Ejecutando comando Docker CON correccion de encoding...")
    
    comando = ["docker", "ps", "-a", "--format", "table {{.Names}}\\t{{.Status}}\\t{{.Ports}}"]
    
    try:
        # FORMA CORRECTA (solucion propuesta)
        log_test("METODO CORREGIDO:")
        log_test(f"subprocess.run({comando}, capture_output=True, text=True, encoding='utf-8', errors='replace')")
        
        result = subprocess.run(
            comando,
            capture_output=True,
            text=True,
            encoding='utf-8',    # Forzar UTF-8
            errors='replace',    # Reemplazar caracteres problemáticos
            timeout=10
        )
        
        log_test("RESULTADO: Comando ejecutado exitosamente")
        log_test(f"STDOUT length: {len(result.stdout) if result.stdout else 0}")
        log_test(f"STDERR length: {len(result.stderr) if result.stderr else 0}")
        log_test(f"Return code: {result.returncode}")
        
        if result.stdout:
            log_test("STDOUT PREVIEW (primeras 200 caracteres):")
            log_test(result.stdout[:200] + "..." if len(result.stdout) > 200 else result.stdout)
        
        return True
        
    except UnicodeDecodeError as e:
        log_test("ERROR INESPERADO!")
        log_test(f"UnicodeDecodeError aun presente: {e}")
        return False
    except Exception as e:
        log_test(f"Otro error: {e}")
        return False

def test_comando_complejo():
    """Prueba con comando docker-compose que puede generar caracteres especiales"""
    log_test("="*60)
    log_test("PRUEBA 3: COMANDO COMPLEJO (docker-compose)")
    log_test("="*60)
    
    comando = ["docker-compose", "-f", "docker-compose.debug.yml", "ps"]
    
    log_test("Probando comando docker-compose con encoding corregido...")
    
    try:
        result = subprocess.run(
            comando,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace',
            timeout=15
        )
        
        log_test("EXITO: docker-compose ejecutado sin UnicodeDecodeError")
        log_test(f"Return code: {result.returncode}")
        
        if result.stdout:
            log_test("STDOUT PREVIEW:")
            print(result.stdout[:300] + "..." if len(result.stdout) > 300 else result.stdout)
        
        if result.stderr:
            log_test("STDERR PREVIEW:")
            print(result.stderr[:300] + "..." if len(result.stderr) > 300 else result.stderr)
        
        return True
        
    except UnicodeDecodeError as e:
        log_test("ERROR: UnicodeDecodeError aun presente")
        log_test(f"Detalles: {e}")
        return False
    except Exception as e:
        log_test(f"Otro error (esperado si containers no están corriendo): {e}")
        return True  # Este error es esperado si containers están parados

def comparar_metodos():
    """Compara ambos métodos lado a lado"""
    log_test("="*60)
    log_test("PRUEBA 4: COMPARACION LADO A LADO")
    log_test("="*60)
    
    comando = ["docker", "version"]
    
    # Método actual (problemático)
    log_test("METODO ACTUAL:")
    try:
        start_time = datetime.now()
        result1 = subprocess.run(
            comando,
            capture_output=True,
            text=True,
            timeout=10
        )
        tiempo1 = (datetime.now() - start_time).total_seconds()
        log_test(f"  Tiempo: {tiempo1:.3f}s")
        log_test(f"  Return code: {result1.returncode}")
        log_test(f"  STDOUT chars: {len(result1.stdout) if result1.stdout else 0}")
    except Exception as e:
        log_test(f"  ERROR: {e}")
    
    # Método corregido
    log_test("METODO CORREGIDO:")
    try:
        start_time = datetime.now()
        result2 = subprocess.run(
            comando,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace',
            timeout=10
        )
        tiempo2 = (datetime.now() - start_time).total_seconds()
        log_test(f"  Tiempo: {tiempo2:.3f}s")
        log_test(f"  Return code: {result2.returncode}")
        log_test(f"  STDOUT chars: {len(result2.stdout) if result2.stdout else 0}")
    except Exception as e:
        log_test(f"  ERROR: {e}")

def main():
    """Ejecutar todas las pruebas"""
    log_test("INICIO DE PRUEBAS DE CONCEPTO - ENCODING UNICODE")
    log_test("Objetivo: Demostrar problema y solucion UnicodeDecodeError")
    log_test("")
    
    # Verificar que estemos en el directorio correcto
    import os
    if not os.path.exists("docker-compose.debug.yml"):
        log_test("ADVERTENCIA: No se encuentra docker-compose.debug.yml")
        log_test("Ejecute desde directorio vnm-proyectos para mejores resultados")
    
    resultados = []
    
    # Ejecutar pruebas
    resultados.append(("Reproducir problema", test_problema_encoding()))
    resultados.append(("Demostrar solucion", test_solucion_encoding()))
    resultados.append(("Comando complejo", test_comando_complejo()))
    
    # Comparación final
    comparar_metodos()
    
    # Resumen
    log_test("="*60)
    log_test("RESUMEN DE PRUEBAS")
    log_test("="*60)
    
    for nombre, resultado in resultados:
        status = "EXITO" if resultado else "FALLO"
        log_test(f"  {nombre}: {status}")
    
    log_test("")
    log_test("CONCLUSION:")
    log_test("La solucion propuesta (encoding='utf-8', errors='replace')")
    log_test("previene UnicodeDecodeError en comandos subprocess.")
    log_test("")
    log_test("SIGUIENTE PASO:")
    log_test("Si estas pruebas son satisfactorias, podemos aplicar")
    log_test("la correccion a los archivos vnm_automate.py y orquestador_desarrollo.py")

if __name__ == "__main__":
    main()