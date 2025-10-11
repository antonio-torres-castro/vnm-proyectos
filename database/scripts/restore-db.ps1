# database\scripts\restore-db.ps1 - VERSION CORREGIDA
param(
    [string]$backupFile = "latest"
)

Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "SISTEMA DE RESTAURACIÓN DE BASE DE DATOS" -ForegroundColor Yellow
Write-Host "=========================================" -ForegroundColor Cyan

# Verificar que Docker esté ejecutándose
try {
    docker version 2>&1 | Out-Null
}
catch {
    Write-Host "ERROR: Docker no está ejecutándose" -ForegroundColor Red
    exit 1
}

if ($backupFile -eq "latest") {
    $latestBackup = Get-ChildItem "..\backups" -Filter "*.sql.zip" | Sort-Object LastWriteTime -Descending | Select-Object -First 1
    if ($latestBackup) {
        $backupFile = $latestBackup.Name
        Write-Host "Usando backup más reciente: $backupFile" -ForegroundColor Cyan
    }
    else {
        Write-Host "ERROR: No se encontraron backups (.sql.zip)" -ForegroundColor Red
        Write-Host "Primero crea un backup con: .\manage-db.ps1 backup" -ForegroundColor Yellow
        exit 1
    }
}

$backupPath = "..\backups\$backupFile"

if (-not (Test-Path $backupPath)) {
    Write-Host "ERROR: Backup no encontrado: $backupFile" -ForegroundColor Red
    Write-Host "`nBackups disponibles:" -ForegroundColor Cyan
    Get-ChildItem "..\backups" -Filter "*.sql.zip" | Sort-Object LastWriteTime -Descending | Format-Table Name, LastWriteTime, @{Name = "Size(MB)"; Expression = { [math]::Round($_.Length / 1MB, 2) } } -AutoSize
    exit 1
}

Write-Host "`nBACKUP SELECCIONADO:" -ForegroundColor White
Write-Host "  Archivo: $backupFile" -ForegroundColor Gray
Write-Host "  Tamaño: $([math]::Round((Get-Item $backupPath).Length/1MB, 2)) MB" -ForegroundColor Gray
Write-Host "  Creado: $((Get-Item $backupPath).LastWriteTime)" -ForegroundColor Gray

Write-Host "`n¡ADVERTENCIA CRÍTICA!" -ForegroundColor Red
Write-Host "====================" -ForegroundColor Red
Write-Host "Esta acción SOBREESCRIBIRÁ COMPLETAMENTE la base de datos actual." -ForegroundColor Red
Write-Host "Todos los datos actuales se perderán y serán reemplazados por el backup." -ForegroundColor Red

$confirmation = Read-Host "`n¿Estás absolutamente seguro? Escribe 'RESTAURAR' para confirmar"
if ($confirmation -ne "RESTAURAR") {
    Write-Host "Restauración cancelada por el usuario" -ForegroundColor Yellow
    exit 0
}

Write-Host "`nIniciando proceso de restauración..." -ForegroundColor Yellow

# Detener servicios dependientes temporalmente
Write-Host "1. Deteniendo servicios dependientes..." -ForegroundColor Cyan
docker stop monitoreo_backend monitoreo_frontend monitoreo_pgadmin 2>$null
Start-Sleep -Seconds 2

# Verificar que PostgreSQL esté ejecutándose
if (-not (docker ps --filter "name=monitoreo_postgres" --format "table {{.Names}}" | Select-String "monitoreo_postgres")) {
    Write-Host "ERROR: PostgreSQL no está ejecutándose" -ForegroundColor Red
    Write-Host "Iniciando PostgreSQL..." -ForegroundColor Yellow
    docker-compose up -d postgres
    Start-Sleep -Seconds 5
}

# Extraer backup comprimido
Write-Host "2. Preparando archivo de backup..." -ForegroundColor Cyan
$tempDir = "..\backups\temp_restore_$(Get-Date -Format 'yyyyMMdd_HHmmss')"
$tempFile = "$tempDir\backup.sql"

try {
    # Extraer el archivo ZIP
    Expand-Archive -Path $backupPath -DestinationPath $tempDir -Force
    
    Write-Host "3. Restaurando base de datos..." -ForegroundColor Cyan
    Write-Host "   Esto puede tomar varios minutos..." -ForegroundColor Yellow
    
    # Restaurar el backup
    Get-Content $tempFile | docker exec -i monitoreo_postgres psql -U monitoreo_user -d postgres -q
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "`n✅ RESTAURACIÓN EXITOSA!" -ForegroundColor Green
        Write-Host "Base de datos restaurada desde: $backupFile" -ForegroundColor White
    }
    else {
        Write-Host "`n❌ ERROR durante la restauración" -ForegroundColor Red
        exit 1
    }
}
catch {
    Write-Host "❌ ERROR: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}
finally {
    # Limpiar directorio temporal
    if (Test-Path $tempDir) {
        Remove-Item $tempDir -Recurse -Force
    }
}

# Reiniciar servicios
Write-Host "4. Reiniciando servicios..." -ForegroundColor Cyan
docker start monitoreo_backend monitoreo_frontend monitoreo_pgadmin 2>$null

Write-Host "`n✅ PROCESO COMPLETADO: $(Get-Date)" -ForegroundColor Green
Write-Host "Todos los servicios están funcionando con los datos restaurados." -ForegroundColor White