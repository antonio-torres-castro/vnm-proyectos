#!/usr/bin/env pwsh
# cerrar-desarrollo.ps1
# Script para cerrar el entorno de desarrollo

param(
    [switch]$LimpiarCompleto,
    [switch]$SoloParar
)

Write-Host "CERRANDO ENTORNO DE DESARROLLO VNM-PROYECTOS" -ForegroundColor Yellow
Write-Host ("=" * 60) -ForegroundColor Yellow

# Verificar que estamos en el directorio correcto
if (-not (Test-Path "docker-compose.debug.yml")) {
    Write-Host "Error: docker-compose.debug.yml no encontrado" -ForegroundColor Red
    Write-Host "Asegurate de estar en el directorio vnm-proyectos" -ForegroundColor Yellow
    exit 1
}

Write-Host "Directorio: $(Get-Location)" -ForegroundColor Green
Write-Host ""

# Mostrar estado actual
Write-Host "Estado actual de contenedores:" -ForegroundColor Cyan
$containers = docker ps --filter "name=vnm_" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
if ($containers) {
    Write-Host $containers -ForegroundColor White
} else {
    Write-Host "   No hay contenedores VNM ejecutandose" -ForegroundColor Gray
}
Write-Host ""

if ($LimpiarCompleto) {
    Write-Host "LIMPIEZA COMPLETA - Eliminando todo..." -ForegroundColor Red
    Write-Host "   - Parando contenedores" -ForegroundColor Yellow
    Write-Host "   - Eliminando volumenes de datos" -ForegroundColor Yellow
    Write-Host "   - Limpiando imagenes no utilizadas" -ForegroundColor Yellow
    Write-Host ""
    
    # Parar y eliminar todo incluyendo volumenes
    docker-compose -f docker-compose.debug.yml down -v
    
    # Limpiar imagenes no utilizadas
    Write-Host "Limpiando imagenes Docker no utilizadas..." -ForegroundColor Yellow
    docker system prune -f | Out-Null
    
    Write-Host "Limpieza completa finalizada" -ForegroundColor Green
    Write-Host ""
    Write-Host "ADVERTENCIA: Todos los datos de la base de datos han sido eliminados" -ForegroundColor Red
    Write-Host "Para reiniciar: .\inicio-desarrollo.ps1" -ForegroundColor Cyan
    
} elseif ($SoloParar) {
    Write-Host "PARADA SIMPLE - Manteniendo datos..." -ForegroundColor Cyan
    Write-Host "   - Parando contenedores" -ForegroundColor Yellow
    Write-Host "   - Manteniendo volumenes de datos" -ForegroundColor Green
    Write-Host ""
    
    # Solo parar contenedores, mantener volumenes
    docker-compose -f docker-compose.debug.yml stop
    
    Write-Host "Contenedores parados (datos preservados)" -ForegroundColor Green
    Write-Host ""
    Write-Host "Para reiniciar rapido: docker-compose -f docker-compose.debug.yml start" -ForegroundColor Cyan
    
} else {
    Write-Host "PARADA NORMAL - Eliminando contenedores, manteniendo datos..." -ForegroundColor Yellow
    Write-Host "   - Parando y eliminando contenedores" -ForegroundColor Yellow
    Write-Host "   - Manteniendo volumenes de datos" -ForegroundColor Green
    Write-Host ""
    
    # Parar y eliminar contenedores pero mantener volumenes
    docker-compose -f docker-compose.debug.yml down
    
    Write-Host "Entorno cerrado (datos preservados)" -ForegroundColor Green
    Write-Host ""
    Write-Host "Para reiniciar: .\inicio-desarrollo.ps1" -ForegroundColor Cyan
}

Write-Host ""

# Verificar estado final
Write-Host "Estado final:" -ForegroundColor Cyan
$remainingContainers = docker ps --filter "name=vnm_" --format "table {{.Names}}\t{{.Status}}"
if ($remainingContainers) {
    Write-Host $remainingContainers -ForegroundColor White
} else {
    Write-Host "   No hay contenedores VNM ejecutandose" -ForegroundColor Green
}

Write-Host ""
Write-Host "OPCIONES DISPONIBLES:" -ForegroundColor Cyan
Write-Host "   Parada simple:      .\cerrar-desarrollo.ps1 -SoloParar" -ForegroundColor White
Write-Host "   Parada normal:      .\cerrar-desarrollo.ps1" -ForegroundColor White  
Write-Host "   Limpieza completa:  .\cerrar-desarrollo.ps1 -LimpiarCompleto" -ForegroundColor White
Write-Host "   Reiniciar:          .\inicio-desarrollo.ps1" -ForegroundColor White
Write-Host ""
Write-Host "Hasta luego!" -ForegroundColor Green
