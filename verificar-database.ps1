#!/usr/bin/env pwsh
# Script de verificación de conexión a base de datos

Write-Host " Verificando conexión a base de datos..." -ForegroundColor Green

# Verificar que los contenedores estén ejecutándose
Write-Host " Estado de contenedores:" -ForegroundColor Cyan
docker-compose -f docker-compose.debug.yml ps

# Verificar logs de postgres
Write-Host "  Últimos logs de PostgreSQL:" -ForegroundColor Cyan
docker logs vnm_postgres_debug --tail 10

# Verificar conectividad de postgres
Write-Host " Verificando conectividad de PostgreSQL..." -ForegroundColor Cyan
$pgReady = docker exec vnm_postgres_debug pg_isready -U monitoreo_user -d monitoreo_dev 2>$null
if ($pgReady) {
    Write-Host " PostgreSQL está listo y acepta conexiones" -ForegroundColor Green
}
else {
    Write-Host " PostgreSQL no está respondiendo" -ForegroundColor Red
    Write-Host " Intenta: docker-compose -f docker-compose.debug.yml restart postgres" -ForegroundColor Yellow
}

# Verificar logs de backend
Write-Host " Últimos logs del Backend:" -ForegroundColor Cyan
docker logs vnm_backend_debug --tail 15

# Verificar si el backend está respondiendo
Write-Host " Verificando API del Backend..." -ForegroundColor Cyan
try {
    $response = Invoke-RestMethod -Uri "http://localhost:8000/api/v1/health" -Method GET -TimeoutSec 5 2>$null
    Write-Host " API del backend está respondiendo" -ForegroundColor Green
    Write-Host " Respuesta: $($response | ConvertTo-Json)" -ForegroundColor White
}
catch {
    Write-Host " API del backend no está respondiendo" -ForegroundColor Red
    Write-Host " Verifica los logs del backend arriba" -ForegroundColor Yellow
}

# Verificar datos en base de datos
Write-Host " Verificando datos en base de datos..." -ForegroundColor Cyan
try {
    $userCount = docker exec vnm_postgres_debug psql -U monitoreo_user -d monitoreo_dev -t -c "SELECT COUNT(*) FROM seguridad.usuario;" 2>$null
    if ($userCount) {
        Write-Host " Tabla de usuarios encontrada. Usuarios: $($userCount.Trim())" -ForegroundColor Green
    }
    else {
        Write-Host "  No se pudo verificar tabla de usuarios" -ForegroundColor Yellow
    }

    $tableCount = docker exec vnm_postgres_debug psql -U monitoreo_user -d monitoreo_dev -t -c "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema='seguridad';" 2>$null
    if ($tableCount) {
        Write-Host " Esquema 'seguridad' encontrado. Tablas: $($tableCount.Trim())" -ForegroundColor Green
    }
    else {
        Write-Host "  Esquema 'seguridad' no encontrado o inaccesible" -ForegroundColor Yellow
    }
}
catch {
    Write-Host " Error al verificar datos en base de datos" -ForegroundColor Red
}

Write-Host " Comandos útiles para debugging:" -ForegroundColor Cyan
Write-Host " Reiniciar postgres: docker-compose -f docker-compose.debug.yml restart postgres" -ForegroundColor White
Write-Host " Ver logs postgres: docker logs vnm_postgres_debug -f" -ForegroundColor White
Write-Host " Ver logs backend: docker logs vnm_backend_debug -f" -ForegroundColor White
Write-Host " Conectar a DB: docker exec -it vnm_postgres_debug psql -U monitoreo_user -d monitoreo_dev" -ForegroundColor White
Write-Host " Limpiar todo: docker-compose -f docker-compose.debug.yml down -v" -ForegroundColor White

Write-Host " Verificación completada!" -ForegroundColor Green
