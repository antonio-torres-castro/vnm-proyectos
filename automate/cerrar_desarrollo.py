#!/usr/bin/env python3
"""
cerrar_desarrollo.py
Script to close the development environment with data preservation options
"""

import subprocess
import sys
import os
import argparse
from pathlib import Path

def run_command(command, shell=True, capture_output=False):
    """Run a command and return the result"""
    try:
        if capture_output:
            result = subprocess.run(command, shell=shell, capture_output=True, text=True)
            return result
        else:
            result = subprocess.run(command, shell=shell)
            return result
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

def stop_simple():
    """Stop containers only, preserve everything"""
    print("SIMPLE STOP - Preserving data...")
    print("   - Stopping containers")
    print("   - Maintaining data volumes")
    print()
    
    result = run_command("docker-compose -f docker-compose.debug.yml stop")
    
    if result and result.returncode == 0:
        print("Containers stopped (data preserved)")
        print()
        print("To restart quickly: docker-compose -f docker-compose.debug.yml start")
    else:
        print("Error stopping containers")

def stop_normal():
    """Stop and remove containers, preserve data volumes"""
    print("NORMAL STOP - Removing containers, maintaining data...")
    print("   - Stopping and removing containers")
    print("   - Maintaining data volumes")
    print()
    
    result = run_command("docker-compose -f docker-compose.debug.yml down")
    
    if result and result.returncode == 0:
        print("Environment closed (data preserved)")
        print()
        print("To restart: python automate/inicio_desarrollo.py")
    else:
        print("Error stopping environment")

def stop_complete():
    """Stop and remove everything including data"""
    print("COMPLETE CLEANUP - Removing everything...")
    print("   - Stopping containers")
    print("   - Removing data volumes")
    print("   - Cleaning unused images")
    print()
    
    # Stop and remove everything including volumes
    result = run_command("docker-compose -f docker-compose.debug.yml down -v")
    
    if result and result.returncode == 0:
        # Clean unused images
        print("Cleaning unused Docker images...")
        run_command("docker system prune -f", capture_output=True)
        
        print("Complete cleanup finished")
        print()
        print("WARNING: All database data has been deleted")
        print("To restart: python automate/inicio_desarrollo.py")
    else:
        print("Error during cleanup")

def main():
    parser = argparse.ArgumentParser(description="Close VNM development environment")
    parser.add_argument("--simple", action="store_true", 
                       help="Only stop containers (fastest restart)")
    parser.add_argument("--complete", action="store_true", 
                       help="Complete cleanup including data volumes")
    
    args = parser.parse_args()
    
    print_header("CLOSING VNM-PROYECTOS DEVELOPMENT ENVIRONMENT")
    print()
    
    # Verify we are in the correct directory
    if not check_file_exists("docker-compose.debug.yml"):
        print("Error: docker-compose.debug.yml not found")
        print("Make sure you are in the vnm-proyectos directory")
        sys.exit(1)
    
    print(f"Directory: {os.getcwd()}")
    print()
    
    # Show current status
    print("Current container status:")
    containers_status = get_containers_status()
    if "No containers found" not in containers_status:
        print(containers_status)
    else:
        print("   No VNM containers running")
    print()
    
    # Execute appropriate action
    if args.complete:
        stop_complete()
    elif args.simple:
        stop_simple()
    else:
        stop_normal()
    
    print()
    
    # Verify final status
    print("Final status:")
    remaining_containers = get_containers_status()
    if "No containers found" not in remaining_containers and remaining_containers != "Error getting container status":
        print(remaining_containers)
    else:
        print("   No VNM containers running")
    
    print()
    print("AVAILABLE OPTIONS:")
    print("   Simple stop:      python automate/cerrar_desarrollo.py --simple")
    print("   Normal stop:      python automate/cerrar_desarrollo.py")
    print("   Complete cleanup: python automate/cerrar_desarrollo.py --complete")
    print("   Restart:          python automate/inicio_desarrollo.py")
    print()
    print("See you later!")

if __name__ == "__main__":
    main()
