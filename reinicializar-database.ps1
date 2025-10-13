# =================================================================
# SCRIPT: REINICIALIZAR BASE DE DATOS CON HASH CORREGIDO
# =================================================================
# Proposito: Reinicializar la BD con el hash bcrypt corregido
# Autor: MiniMax Agent
# Fecha: 2025-10-14

Write-Host "Reinicializando base de datos con hash corregido..." -ForegroundColor Yellow
Write-Host "==============================================" -ForegroundColor Yellow

# 1. Detener contenedores
Write-Host "1. Deteniendo contenedores..." -ForegroundColor Cyan
docker-compose -f docker-compose.debug.yml down -v

# 2. Reiniciar contenedores (esto ejecutará automáticamente los scripts SQL)
Write-Host "2. Iniciando contenedores con BD limpia..." -ForegroundColor Cyan
docker-compose -f docker-compose.debug.yml up -d postgres

# 3. Esperar que PostgreSQL esté listo
Write-Host "3. Esperando que PostgreSQL esté listo..." -ForegroundColor Cyan
$maxIntentos = 30
$intento = 0
$pgListo = $false

do {
    $intento++
    try {
        $testResult = docker exec vnm_postgres_debug pg_isready -U monitoreo_user -d monitoreo_dev 2>$null
        if ($LASTEXITCODE -eq 0) {
            $pgListo = $true
            Write-Host "PostgreSQL listo!" -ForegroundColor Green
        } else {
            Write-Host "Esperando PostgreSQL... ($intento/$maxIntentos)" -ForegroundColor Yellow
            Start-Sleep -Seconds 2
        }
    } catch {
        Write-Host "Esperando PostgreSQL... ($intento/$maxIntentos)" -ForegroundColor Yellow
        Start-Sleep -Seconds 2
    }
} while (-not $pgListo -and $intento -lt $maxIntentos)

if (-not $pgListo) {
    Write-Host "Error: PostgreSQL no respondió en tiempo esperado" -ForegroundColor Red
    exit 1
}

# 4. Verificar que el usuario está correctamente creado
Write-Host "4. Verificando usuario en BD..." -ForegroundColor Cyan
$verificarSQL = "SELECT email, LENGTH(clave_hash) as hash_length, LEFT(clave_hash, 10) as hash_start FROM seguridad.usuario WHERE email = 'admin@monitoreo.cl';"
$verificarResult = docker exec vnm_postgres_debug psql -U monitoreo_user -d monitoreo_dev -c $verificarSQL

if ($LASTEXITCODE -eq 0) {
    Write-Host "Usuario verificado exitosamente:" -ForegroundColor Green
    Write-Host "$verificarResult" -ForegroundColor Gray
} else {
    Write-Host "Error al verificar usuario: $verificarResult" -ForegroundColor Red
    exit 1
}

# 5. Iniciar todos los servicios
Write-Host "5. Iniciando todos los servicios..." -ForegroundColor Cyan
docker-compose -f docker-compose.debug.yml up -d

Write-Host "" -ForegroundColor White
Write-Host "RESUMEN:" -ForegroundColor Green
Write-Host "========" -ForegroundColor Green
Write-Host "Base de datos reinicializada exitosamente" -ForegroundColor Green
Write-Host "Hash bcrypt corregido aplicado" -ForegroundColor Green
Write-Host "Credenciales de acceso:" -ForegroundColor Cyan
Write-Host "  Email: admin@monitoreo.cl" -ForegroundColor White
Write-Host "  Password: admin123" -ForegroundColor White
Write-Host "  URL: http://localhost:8000/api/v1/auth/login" -ForegroundColor White
Write-Host "" -ForegroundColor White
Write-Host "Reinicializacion completada!" -ForegroundColor Green