#!/usr/bin/env pwsh
# inicio-desarrollo-seguro.ps1
# Script de inicio con deteccion y solucion automatica de errores comunes

Write-Host "INICIANDO ENTORNO DE DESARROLLO VNM-PROYECTOS (MODO SEGURO)" -ForegroundColor Cyan
Write-Host ("=" * 65) -ForegroundColor Cyan

# Verificar que estamos en el directorio correcto
if (-not (Test-Path "docker-compose.debug.yml")) {
    Write-Host "Error: docker-compose.debug.yml no encontrado" -ForegroundColor Red
    Write-Host "Asegurate de estar en el directorio vnm-proyectos" -ForegroundColor Yellow
    exit 1
}

Write-Host "Directorio: $(Get-Location)" -ForegroundColor Green
Write-Host ""

# Funcion para verificar errores comunes en logs
function Test-CommonErrors($containerName) {
    $logs = docker logs $containerName 2>&1
    $hasErrors = $false
    
    if ($logs -match "bcrypt.*error|Traceback.*bcrypt") {
        Write-Host "   DETECTADO: Error de bcrypt en $containerName" -ForegroundColor Red
        $hasErrors = $true
    }
    
    if ($logs -match "ModuleNotFoundError|ImportError") {
        Write-Host "   DETECTADO: Error de modulos Python en $containerName" -ForegroundColor Red
        $hasErrors = $true
    }
    
    if ($logs -match "connection.*refused|Connection.*failed") {
        Write-Host "   DETECTADO: Error de conexion en $containerName" -ForegroundColor Red
        $hasErrors = $true
    }
    
    return $hasErrors
}

# Paso 1: Limpiar entorno previo
Write-Host "Paso 1: Limpiando entorno previo..." -ForegroundColor Yellow
docker-compose -f docker-compose.debug.yml down -v | Out-Null
Start-Sleep -Seconds 2

# Paso 2: Verificar si necesitamos reconstruir imagenes
Write-Host "Paso 2: Verificando necesidad de reconstruccion..." -ForegroundColor Yellow
$needsRebuild = $false

# Verificar si existen imagenes previas con problemas
$backendImage = docker images --filter "reference=vnm-proyectos-backend" --quiet
if ($backendImage) {
    Write-Host "   Imagen backend existente detectada" -ForegroundColor Gray
    
    # Test rapido para detectar problemas potenciales
    Write-Host "   Probando imagen backend existente..." -ForegroundColor Gray
    docker run --rm $backendImage python -c "import bcrypt; print('bcrypt OK')" 2>$null
    if (-not $?) {
        Write-Host "   PROBLEMA detectado en imagen backend - se reconstruira" -ForegroundColor Yellow
        $needsRebuild = $true
    } else {
        Write-Host "   Imagen backend parece estar bien" -ForegroundColor Green
    }
}

# Paso 3: Reconstruir si es necesario
if ($needsRebuild) {
    Write-Host "Paso 3: Reconstruyendo imagen backend..." -ForegroundColor Yellow
    Write-Host "   Esto corrige problemas de dependencias automaticamente" -ForegroundColor Cyan
    docker-compose -f docker-compose.debug.yml build --no-cache backend
    
    if (-not $?) {
        Write-Host "   ERROR: Fallo la reconstruccion del backend" -ForegroundColor Red
        Write-Host "   Ejecuta manualmente: .\fix-bcrypt-error.ps1" -ForegroundColor Yellow
        exit 1
    }
    Write-Host "   Imagen backend reconstruida exitosamente" -ForegroundColor Green
} else {
    Write-Host "Paso 3: Imagen backend OK - no necesita reconstruccion" -ForegroundColor Green
}

# Paso 4: Iniciar servicios
Write-Host "Paso 4: Iniciando servicios..." -ForegroundColor Yellow
Write-Host "   - PostgreSQL Database"
Write-Host "   - Backend FastAPI (modo debug)"
Write-Host "   - Frontend React"
Write-Host ""

docker-compose -f docker-compose.debug.yml up -d

# Paso 5: Esperar y verificar servicios
Write-Host "Paso 5: Esperando a que los servicios esten listos..." -ForegroundColor Yellow

$timeout = 90
$elapsed = 0
$allReady = $false

while (-not $allReady -and $elapsed -lt $timeout) {
    $postgres = docker exec vnm_postgres_debug pg_isready -U monitoreo_user -d monitoreo_dev 2>$null
    $backend = docker ps --filter "name=vnm_backend_debug" --filter "status=running" --quiet
    $frontend = docker ps --filter "name=vnm_frontend_debug" --filter "status=running" --quiet
    
    if ($postgres -match "accepting connections" -and $backend -and $frontend) {
        # Verificar errores comunes en backend
        if (Test-CommonErrors "vnm_backend_debug") {
            Write-Host "   Errores detectados en backend - aplicando solucion..." -ForegroundColor Yellow
            docker-compose -f docker-compose.debug.yml restart backend
            Start-Sleep -Seconds 10
        }
        
        # Verificar nuevamente
        if (-not (Test-CommonErrors "vnm_backend_debug")) {
            $allReady = $true
        }
    } else {
        Write-Host "   Esperando servicios... ($elapsed/$timeout s)" -ForegroundColor Gray
        Start-Sleep -Seconds 5
        $elapsed += 5
    }
}

if (-not $allReady) {
    Write-Host "Timeout: Los servicios tardaron mas de lo esperado" -ForegroundColor Red
    Write-Host "Diagnostico automatico:" -ForegroundColor Yellow
    
    # Diagnostico automatico de problemas
    Write-Host "   Backend logs:" -ForegroundColor Cyan
    docker logs vnm_backend_debug --tail 10
    
    Write-Host "   Sugerencias:" -ForegroundColor Cyan
    Write-Host "   1. Ejecutar: .\fix-bcrypt-error.ps1" -ForegroundColor White
    Write-Host "   2. Verificar: docker ps" -ForegroundColor White
    Write-Host "   3. Ver logs: docker logs vnm_backend_debug -f" -ForegroundColor White
    
} else {
    Write-Host "Todos los servicios estan listos y sin errores criticos!" -ForegroundColor Green
}

Write-Host ""

# Paso 6: Mostrar estado
Write-Host "Paso 6: Estado de los servicios:" -ForegroundColor Yellow
Write-Host ""

$containers = docker ps --filter "name=vnm_" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
Write-Host $containers -ForegroundColor White

Write-Host ""

# Paso 7: Verificacion final de salud
Write-Host "Paso 7: Verificacion final de salud..." -ForegroundColor Yellow

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

# Test Backend (errores criticos)
$backendErrors = Test-CommonErrors "vnm_backend_debug"
if (-not $backendErrors) {
    Write-Host "   Backend API: En modo debug - sin errores criticos" -ForegroundColor Green
    Write-Host "     Para activar: F5 en VS Code -> Backend: FastAPI Docker Debug" -ForegroundColor Cyan
} else {
    Write-Host "   Backend API: ERRORES DETECTADOS - revisar logs" -ForegroundColor Red
    Write-Host "     Solucion: .\fix-bcrypt-error.ps1" -ForegroundColor Yellow
}

Write-Host ""

# Resumen final
Write-Host "ENTORNO LISTO PARA DESARROLLO (MODO SEGURO)" -ForegroundColor Green
Write-Host ("=" * 45) -ForegroundColor Green
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
Write-Host "   Solucionar bcrypt: .\fix-bcrypt-error.ps1" -ForegroundColor White
Write-Host ""
Write-Host "Desarrollo seguro activado!" -ForegroundColor Green
