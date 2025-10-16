#!/usr/bin/env python3
"""
inicio_desarrollo.py
Script to start the complete development environment
"""

import subprocess
import sys
import os
import time
import requests
from pathlib import Path

def run_command(command, shell=True, capture_output=False, timeout=None):
    """Run a command and return the result"""
    try:
        if capture_output:
            result = subprocess.run(command, shell=shell, capture_output=True, 
                                  text=True, timeout=timeout)
            return result
        else:
            result = subprocess.run(command, shell=shell, timeout=timeout)
            return result
    except subprocess.TimeoutExpired:
        print(f"Timeout: Command took too long: {command}")
        return None
    except Exception as e:
        print(f"Error running command: {command}")
        print(f"Error: {e}")
        return None

def check_file_exists(file_path):
    """Check if a file exists"""
    return Path(file_path).exists()

def print_header(text):
    """Print a header with separator"""
    print(text)
    print("=" * len(text))

def print_step(step_number, description):
    """Print a step description"""
    print(f"Step {step_number}: {description}")

def check_postgres_ready():
    """Check if PostgreSQL is ready"""
    try:
        result = run_command(
            'docker exec vnm_postgres_debug pg_isready -U monitoreo_user -d monitoreo_dev',
            capture_output=True
        )
        if result and result.returncode == 0:
            return "accepting connections" in result.stdout
        return False
    except:
        return False

def check_container_running(container_name):
    """Check if a container is running"""
    try:
        result = run_command(
            f'docker ps --filter "name={container_name}" --filter "status=running" --quiet',
            capture_output=True
        )
        if result and result.returncode == 0:
            return len(result.stdout.strip()) > 0
        return False
    except:
        return False

def check_http_service(url, timeout=5):
    """Check if HTTP service is available"""
    try:
        response = requests.get(url, timeout=timeout)
        return response.status_code == 200
    except:
        return False

def get_containers_status():
    """Get status of VNM containers"""
    try:
        result = run_command(
            'docker ps --filter "name=vnm_" --format "table {{.Names}}\\t{{.Status}}\\t{{.Ports}}"',
            capture_output=True
        )
        if result and result.returncode == 0:
            return result.stdout.strip()
        return "No containers found"
    except:
        return "Error getting container status"

def main():
    """Main function to start development environment"""
    
    print_header("STARTING VNM-PROYECTOS DEVELOPMENT ENVIRONMENT")
    print()
    
    # Verify we are in the correct directory
    if not check_file_exists("docker-compose.debug.yml"):
        print("Error: docker-compose.debug.yml not found")
        print("Make sure you are in the vnm-proyectos directory")
        sys.exit(1)
    
    print(f"Directory: {os.getcwd()}")
    print()
    
    # Step 1: Clean previous environment if exists
    print_step(1, "Cleaning previous environment...")
    print("   Stopping containers (preserving data)...")
    result = run_command("docker-compose -f docker-compose.debug.yml down")
    time.sleep(2)
    
    # Step 2: Install frontend dependencies
    print_step(2, "Installing frontend dependencies...")
    if check_file_exists("frontend/package.json"):
        print("   Installing Node.js dependencies...")
        result = run_command("cd frontend && npm install")
        if result and result.returncode != 0:
            print("   Warning: npm install failed, continuing anyway")
        else:
            print("   Dependencies installed successfully")
    else:
        print("   frontend/package.json not found, skipping")
    print()
    
    # Step 3: Start services
    print_step(3, "Starting services...")
    print("   - PostgreSQL Database")
    print("   - Backend FastAPI (debug mode)")
    print("   - Frontend React")
    print()
    
    result = run_command("docker-compose -f docker-compose.debug.yml up -d")
    
    if result and result.returncode != 0:
        print("Error starting services")
        sys.exit(1)
    
    # Step 4: Wait for services to be ready
    print_step(4, "Waiting for services to be ready...")
    
    timeout = 60
    elapsed = 0
    all_ready = False
    
    while not all_ready and elapsed < timeout:
        postgres_ready = check_postgres_ready()
        backend_running = check_container_running("vnm_backend_debug")
        frontend_running = check_container_running("vnm_frontend_debug")
        
        if postgres_ready and backend_running and frontend_running:
            all_ready = True
        else:
            print("   Waiting for services...")
            time.sleep(5)
            elapsed += 5
    
    if not all_ready:
        print("Timeout: Services took longer than expected")
        print("Check manually with: docker ps")
    else:
        print("All services are ready!")
    
    print()
    
    # Step 5: Show status
    print_step(5, "Service status:")
    print()
    
    containers_status = get_containers_status()
    print(containers_status)
    
    print()
    
    # Step 6: Verify connectivity
    print_step(6, "Verifying connectivity...")
    
    # Test PostgreSQL
    if check_postgres_ready():
        print("   PostgreSQL: Connected and ready")
    else:
        print("   PostgreSQL: Not responding")
    
    # Test Frontend
    if check_http_service("http://localhost:3000"):
        print("   Frontend React: Available at http://localhost:3000")
    else:
        print("   Frontend React: Starting... (try http://localhost:3000 in 30s)")
    
    # Test Backend (in debug mode, will wait for VS Code)
    print("   Backend API: In debug mode - waiting for VS Code")
    print("     To activate: F5 in VS Code -> Backend: FastAPI Docker Debug")
    
    print()
    
    # Final summary
    print_header("DEVELOPMENT ENVIRONMENT READY")
    print()
    print("NEXT STEPS:")
    print("   1. Open VS Code in this directory: code .")
    print("   2. Press F5 to start debugging")
    print("   3. Select: Backend: FastAPI Docker Debug")
    print("   4. The API will activate at http://localhost:8000")
    print()
    print("AVAILABLE SERVICES:")
    print("   Frontend:     http://localhost:3000")
    print("   Backend API:  http://localhost:8000 (after F5)")
    print("   PostgreSQL:   localhost:5432")
    print("   Debug Server: localhost:5678")
    print()
    print("USEFUL COMMANDS:")
    print("   View backend logs:  docker logs vnm_backend_debug -f")
    print("   View postgres logs: docker logs vnm_postgres_debug -f")
    print("   Close (save data):  python automate/cerrar_desarrollo.py")
    print("   Quick stop:         python automate/cerrar_desarrollo.py --simple")
    print("   Check status:       python automate/verificar_configuracion_completa.py")
    print()
    print("Happy development!")

if __name__ == "__main__":
    main()
