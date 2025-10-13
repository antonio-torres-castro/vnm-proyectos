#!/usr/bin/env pwsh
# inicio-desarrollo.ps1
# Script para iniciar el entorno de desarrollo completo

Write-Host "INICIANDO ENTORNO DE DESARROLLO VNM-PROYECTOS" -ForegroundColor Cyan
Write-Host ("=" * 60) -ForegroundColor Cyan

# Verificar que estamos en el directorio correcto
if (-not (Test-Path "docker-compose.debug.yml")) {
    Write-Host "Error: docker-compose.debug.yml no encontrado" -ForegroundColor Red
    Write-Host "Asegurate de estar en el directorio vnm-proyectos" -ForegroundColor Yellow
    exit 1
}

Write-Host "Directorio: $(Get-Location)" -ForegroundColor Green
Write-Host ""

# Paso 1: Limpiar entorno previo si existe
Write-Host "Paso 1: Limpiando entorno previo..." -ForegroundColor Yellow
docker-compose -f docker-compose.debug.yml down -v | Out-Null
Start-Sleep -Seconds 2

# Paso 2: Levantar servicios
Write-Host "Paso 2: Iniciando servicios..." -ForegroundColor Yellow
Write-Host "   - PostgreSQL Database"
Write-Host "   - Backend FastAPI (modo debug)"
Write-Host "   - Frontend React"
Write-Host ""

docker-compose -f docker-compose.debug.yml up -d

# Paso 3: Esperar a que los servicios esten listos
Write-Host "Paso 3: Esperando a que los servicios esten listos..." -ForegroundColor Yellow

$timeout = 60
$elapsed = 0
$allReady = $false

while (-not $allReady -and $elapsed -lt $timeout) {
    $postgres = docker exec vnm_postgres_debug pg_isready -U monitoreo_user -d monitoreo_dev 2>$null
    $backend = docker ps --filter "name=vnm_backend_debug" --filter "status=running" --quiet
    $frontend = docker ps --filter "name=vnm_frontend_debug" --filter "status=running" --quiet
    
    if ($postgres -match "accepting connections" -and $backend -and $frontend) {
        $allReady = $true
    } else {
        Write-Host "   Esperando servicios..." -ForegroundColor Gray
        Start-Sleep -Seconds 5
        $elapsed += 5
    }
}

if (-not $allReady) {
    Write-Host "Timeout: Los servicios tardaron mas de lo esperado" -ForegroundColor Red
    Write-Host "Verifica manualmente con: docker ps" -ForegroundColor Yellow
} else {
    Write-Host "Todos los servicios estan listos!" -ForegroundColor Green
}

Write-Host ""

# Paso 4: Mostrar estado
Write-Host "Paso 4: Estado de los servicios:" -ForegroundColor Yellow
Write-Host ""

$containers = docker ps --filter "name=vnm_" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
Write-Host $containers -ForegroundColor White

Write-Host ""

# Paso 5: Verificar conectividad
Write-Host "Paso 5: Verificando conectividad..." -ForegroundColor Yellow

# Test PostgreSQL
try {
    $pgTest = docker exec vnm_postgres_debug pg_isready -U monitoreo_user -d monitoreo_dev 2>$null
    if ($pgTest -match "accepting connections") {
        Write-Host "   PostgreSQL: Conectado y listo" -ForegroundColor Green
    } else {
        Write-Host "   PostgreSQL: No responde" -ForegroundColor Red
    }
} catch {
    Write-Host "   PostgreSQL: Error de conexion" -ForegroundColor Red
}

# Test Frontend
try {
    $frontendTest = Invoke-WebRequest -Uri "http://localhost:3000" -TimeoutSec 5 -UseBasicParsing
    if ($frontendTest.StatusCode -eq 200) {
        Write-Host "   Frontend React: Disponible en http://localhost:3000" -ForegroundColor Green
    }
} catch {
    Write-Host "   Frontend React: Iniciando... (prueba http://localhost:3000 en 30s)" -ForegroundColor Yellow
}

# Test Backend (solo en modo normal, en debug esperara VS Code)
Write-Host "   Backend API: En modo debug - esperando VS Code" -ForegroundColor Yellow
Write-Host "     Para activar: F5 en VS Code -> Backend: FastAPI Docker Debug" -ForegroundColor Cyan

Write-Host ""

# Resumen final
Write-Host "ENTORNO LISTO PARA DESARROLLO" -ForegroundColor Green
Write-Host ("=" * 40) -ForegroundColor Green
Write-Host ""
Write-Host "PROXIMOS PASOS:" -ForegroundColor Cyan
Write-Host "   1. Abrir VS Code en este directorio: code ." -ForegroundColor White
Write-Host "   2. Presionar F5 para iniciar debugging" -ForegroundColor White  
Write-Host "   3. Seleccionar: Backend: FastAPI Docker Debug" -ForegroundColor White
Write-Host "   4. La API se activara en http://localhost:8000" -ForegroundColor White
Write-Host ""
Write-Host "SERVICIOS DISPONIBLES:" -ForegroundColor Cyan
Write-Host "   Frontend:     http://localhost:3000" -ForegroundColor White
Write-Host "   Backend API:  http://localhost:8000 (despues de F5)" -ForegroundColor White
Write-Host "   PostgreSQL:   localhost:5432" -ForegroundColor White
Write-Host "   Debug Server: localhost:5678" -ForegroundColor White
Write-Host ""
Write-Host "COMANDOS UTILES:" -ForegroundColor Cyan
Write-Host "   Ver logs backend:  docker logs vnm_backend_debug -f" -ForegroundColor White
Write-Host "   Ver logs postgres: docker logs vnm_postgres_debug -f" -ForegroundColor White
Write-Host "   Parar todo:        docker-compose -f docker-compose.debug.yml down" -ForegroundColor White
Write-Host "   Verificar estado:  .\verificar-database.ps1" -ForegroundColor White
Write-Host ""
Write-Host "Feliz desarrollo!" -ForegroundColor Green
