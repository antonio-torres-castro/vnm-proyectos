# database\scripts\backup-db.ps1 - VERSION CORREGIDA
param()

$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$backupFile = "backup_$timestamp.sql"
$backupPath = "..\backups\$backupFile"

Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "CREANDO BACKUP DE BASE DE DATOS..." -ForegroundColor Yellow
Write-Host "=========================================" -ForegroundColor Cyan

# Verificar que Docker esté ejecutándose
try {
    docker version 2>&1 | Out-Null
}
catch {
    Write-Host "ERROR: Docker no está ejecutándose" -ForegroundColor Red
    exit 1
}

# Verificar que el contenedor esté ejecutándose
if (-not (docker ps --filter "name=monitoreo_postgres" --format "table {{.Names}}" | Select-String "monitoreo_postgres")) {
    Write-Host "ERROR: El contenedor monitoreo_postgres no está en ejecución" -ForegroundColor Red
    Write-Host "Ejecuta primero: docker-compose up -d" -ForegroundColor Yellow
    exit 1
}

Write-Host "Contenedor PostgreSQL encontrado, creando backup..." -ForegroundColor Green

# Crear backup usando pg_dumpall para respaldar TODAS las bases de datos
Write-Host "Ejecutando pg_dumpall..." -ForegroundColor Cyan
docker exec monitoreo_postgres pg_dumpall -U monitoreo_user -c > $backupPath

# Verificar que el backup se creó
if (Test-Path $backupPath) {
    $fileSize = (Get-Item $backupPath).Length / 1MB
    $fileSizeRounded = [math]::Round($fileSize, 2)
    
    if ($fileSize -gt 0) {
        Write-Host "BACKUP CREADO EXITOSAMENTE!" -ForegroundColor Green
        Write-Host "Archivo: $backupFile" -ForegroundColor White
        Write-Host "Tamaño: $fileSizeRounded MB" -ForegroundColor White
        Write-Host "Ubicación: $((Resolve-Path $backupPath).Path)" -ForegroundColor Gray
        
        # Comprimir el backup (usar .zip en lugar de .gz)
        Write-Host "Comprimiendo backup..." -ForegroundColor Cyan
        $zipPath = "$backupPath.zip"
        Compress-Archive -Path $backupPath -DestinationPath $zipPath -Force
        Remove-Item $backupPath -Force
        
        # Mantener solo últimos 10 backups
        $backups = Get-ChildItem "..\backups" -Filter "*.sql.zip" | Sort-Object LastWriteTime -Descending
        if ($backups.Count -gt 10) {
            $oldBackups = $backups | Select-Object -Skip 10
            $oldBackups | Remove-Item -Force
            Write-Host "Eliminados $($oldBackups.Count) backups antiguos (manteniendo últimos 10)" -ForegroundColor Yellow
        }
        
        Write-Host "`nResumen de backups:" -ForegroundColor Cyan
        Get-ChildItem "..\backups" -Filter "*.sql.zip" | Sort-Object LastWriteTime -Descending | Format-Table Name, LastWriteTime, @{Name = "Size(MB)"; Expression = { [math]::Round($_.Length / 1MB, 2) } } -AutoSize
        
    }
    else {
        Write-Host "ERROR: El backup está vacío o corrupto" -ForegroundColor Red
        Remove-Item $backupPath -Force
        exit 1
    }
}
else {
    Write-Host "ERROR: No se pudo crear el backup" -ForegroundColor Red
    exit 1
}

Write-Host "`nBackup completado: $(Get-Date)" -ForegroundColor Green