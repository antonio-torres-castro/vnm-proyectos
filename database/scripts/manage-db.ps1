# database\scripts\manage-db.ps1 - VERSION CORREGIDA
param(
    [string]$Action = "help"
)

switch ($Action.ToLower()) {
    "backup" {
        Write-Host "EJECUTANDO BACKUP..." -ForegroundColor Cyan
        & ".\backup-db.ps1"
    }
    "restore" {
        Write-Host "EJECUTANDO RESTAURACION..." -ForegroundColor Cyan
        & ".\restore-db.ps1"
    }
    "restore-specific" {
        $backupFile = Read-Host "Ingresa el nombre del backup (ej: backup_20241010_143022.sql)"
        & ".\restore-db.ps1" -backupFile $backupFile
    }
    "list-backups" {
        Write-Host "BACKUPS DISPONIBLES:" -ForegroundColor Cyan
        Get-ChildItem "..\backups" -Filter "*.sql" | Sort-Object LastWriteTime -Descending | Format-Table Name, LastWriteTime, @{Name = "Size(MB)"; Expression = { [math]::Round($_.Length / 1MB, 2) } } -AutoSize
    }
    "status" {
        Write-Host "ESTADO DE LA BASE DE DATOS:" -ForegroundColor Cyan
        Set-Location "..\.."
        docker-compose ps
        Write-Host "`nBACKUPS:" -ForegroundColor Cyan
        Set-Location "database\scripts"
        & ".\manage-db.ps1" "list-backups"
    }
    "auto-backup" {
        & ".\backup-db.ps1"
    }
    "start" {
        Write-Host "INICIANDO TODOS LOS SERVICIOS..." -ForegroundColor Cyan
        Set-Location "..\.."
        docker-compose up -d
        Write-Host "SERVICIOS INICIADOS" -ForegroundColor Green
        Write-Host "PgAdmin: http://localhost:8081" -ForegroundColor Yellow
        Write-Host "Backend: http://localhost:8000" -ForegroundColor Yellow
        Write-Host "Frontend: http://localhost:3000" -ForegroundColor Yellow
        Write-Host "API Docs: http://localhost:8000/docs" -ForegroundColor Yellow
    }
    "safe-shutdown" {
        Write-Host "APAGADO SEGURO..." -ForegroundColor Cyan
        Set-Location "..\.."
        
        # Backup antes de apagar
        Write-Host "CREANDO BACKUP DE SEGURIDAD..." -ForegroundColor Yellow
        Set-Location "database\scripts"
        & ".\backup-db.ps1"
        
        # Apagar contenedores
        Set-Location "..\.."
        docker-compose down
        
        Write-Host "SISTEMA APAGADO SEGURAMENTE" -ForegroundColor Green
    }
    "restart" {
        Write-Host "REINICIANDO SISTEMA..." -ForegroundColor Cyan
        Set-Location "..\.."
        docker-compose restart
        Write-Host "SISTEMA REINICIADO" -ForegroundColor Green
    }
    "logs" {
        Write-Host "MOSTRANDO LOGS..." -ForegroundColor Cyan
        Set-Location "..\.."
        docker-compose logs -f
    }
    "setup-pgadmin" {
        Write-Host "CONFIGURANDO PGADMIN PERSISTENTE..." -ForegroundColor Cyan
        Set-Location "..\.."
        
        # Parar servicios
        docker-compose down
        
        # Crear estructura si no existe
        if (-not (Test-Path "database\pgadmin-data")) {
            New-Item -ItemType Directory -Path "database\pgadmin-data" -Force
        }
        
        # Iniciar con nueva configuracion
        docker-compose up -d
        
        Write-Host "PGADMIN CONFIGURADO CON PERSISTENCIA" -ForegroundColor Green
        Write-Host "Accede a: http://localhost:8081" -ForegroundColor Yellow
        Write-Host "Usuario: admin@monitoreo.cl" -ForegroundColor White
        Write-Host "Password: admin123" -ForegroundColor White
    }
    default {
        Write-Host "SISTEMA DE GESTION - MONITOREO RED IP" -ForegroundColor Yellow
        Write-Host "==============================================" -ForegroundColor Yellow
        Write-Host "COMANDOS DISPONIBLES:" -ForegroundColor White
        Write-Host "  .\manage-db.ps1 start           - Iniciar todos los servicios"
        Write-Host "  .\manage-db.ps1 safe-shutdown   - Apagar con backup automatico"
        Write-Host "  .\manage-db.ps1 restart         - Reiniciar servicios"
        Write-Host "  .\manage-db.ps1 backup          - Crear backup manual"
        Write-Host "  .\manage-db.ps1 restore         - Restaurar ultimo backup"
        Write-Host "  .\manage-db.ps1 status          - Estado del sistema"
        Write-Host "  .\manage-db.ps1 list-backups    - Listar backups"
        Write-Host "  .\manage-db.ps1 logs            - Ver logs en tiempo real"
        Write-Host "  .\manage-db.ps1 setup-pgadmin   - Configurar PgAdmin persistente"
        Write-Host ""
        Write-Host "FLUJO RECOMENDADO:" -ForegroundColor Gray
        Write-Host "  cd database\scripts"
        Write-Host "  .\manage-db.ps1 setup-pgadmin    (solo primera vez)"
        Write-Host "  .\manage-db.ps1 start"
        Write-Host "  .\manage-db.ps1 safe-shutdown"
    }
}