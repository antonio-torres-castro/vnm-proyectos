#!/usr/bin/env pwsh
# fix-bcrypt-error.ps1
# Script para solucionar el error de bcrypt en el backend

Write-Host "SOLUCIONANDO ERROR DE BCRYPT" -ForegroundColor Cyan
Write-Host ("=" * 50) -ForegroundColor Cyan

# Verificar que estamos en el directorio correcto
if (-not (Test-Path "docker-compose.debug.yml")) {
    Write-Host "Error: docker-compose.debug.yml no encontrado" -ForegroundColor Red
    Write-Host "Asegurate de estar en el directorio vnm-proyectos" -ForegroundColor Yellow
    exit 1
}

Write-Host "Directorio: $(Get-Location)" -ForegroundColor Green
Write-Host ""

# Paso 1: Parar contenedores actuales
Write-Host "Paso 1: Parando contenedores actuales..." -ForegroundColor Yellow
docker-compose -f docker-compose.debug.yml down

# Paso 2: Limpiar imagenes existentes del backend
Write-Host "Paso 2: Limpiando imagen del backend..." -ForegroundColor Yellow
$backendImage = docker images --filter "reference=vnm-proyectos-backend" --quiet
if ($backendImage) {
    Write-Host "Removiendo imagen existente del backend..." -ForegroundColor Yellow
    docker rmi $backendImage -f
} else {
    Write-Host "No se encontro imagen existente del backend" -ForegroundColor Gray
}

# Paso 3: Reconstruir imagen del backend con dependencias corregidas
Write-Host "Paso 3: Reconstruyendo imagen del backend..." -ForegroundColor Yellow
Write-Host "Esto incluye:" -ForegroundColor Cyan
Write-Host "  - Herramientas de compilacion para bcrypt" -ForegroundColor White
Write-Host "  - Dependencias actualizadas" -ForegroundColor White
Write-Host "  - Bcrypt version estable" -ForegroundColor White
Write-Host ""

docker-compose -f docker-compose.debug.yml build --no-cache backend

# Verificar si la construccion fue exitosa
$buildResult = $?
if (-not $buildResult) {
    Write-Host "Error: Fallo la construccion del backend" -ForegroundColor Red
    Write-Host "Verifica los logs arriba para mas detalles" -ForegroundColor Yellow
    exit 1
}

# Paso 4: Iniciar contenedores con imagen corregida
Write-Host "Paso 4: Iniciando contenedores con imagen corregida..." -ForegroundColor Yellow
docker-compose -f docker-compose.debug.yml up -d

# Paso 5: Esperar y verificar que el backend inicie correctamente
Write-Host "Paso 5: Verificando que el backend inicie sin errores..." -ForegroundColor Yellow

Start-Sleep -Seconds 10

# Verificar logs del backend para errores de bcrypt
Write-Host "Verificando logs del backend..." -ForegroundColor Cyan
$backendLogs = docker logs vnm_backend_debug 2>&1
if ($backendLogs -match "bcrypt.*error|Traceback.*bcrypt") {
    Write-Host "ADVERTENCIA: Aun se detectan errores de bcrypt en los logs" -ForegroundColor Red
    Write-Host "Logs del backend:" -ForegroundColor Yellow
    docker logs vnm_backend_debug --tail 20
} else {
    Write-Host "Backend iniciando correctamente sin errores de bcrypt" -ForegroundColor Green
}

# Paso 6: Verificar estado final
Write-Host "Paso 6: Estado final de contenedores:" -ForegroundColor Yellow
docker ps --filter "name=vnm_" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

Write-Host ""
Write-Host "SOLUCION DE BCRYPT COMPLETADA" -ForegroundColor Green
Write-Host ("=" * 40) -ForegroundColor Green
Write-Host ""

Write-Host "PROXIMOS PASOS:" -ForegroundColor Cyan
Write-Host "1. Verificar que no hay errores: .\verificar-database.ps1" -ForegroundColor White
Write-Host "2. Abrir VS Code: code ." -ForegroundColor White
Write-Host "3. Iniciar debugging: F5 -> Backend: FastAPI Docker Debug" -ForegroundColor White
Write-Host ""

Write-Host "Si el problema persiste:" -ForegroundColor Yellow
Write-Host "  - Ejecuta: docker logs vnm_backend_debug -f" -ForegroundColor White
Write-Host "  - Revisa los logs para errores especificos" -ForegroundColor White
Write-Host ""

Write-Host "Solucion aplicada!" -ForegroundColor Green
