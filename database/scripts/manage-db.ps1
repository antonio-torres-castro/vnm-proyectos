# Sistema de Gestión de Base de Datos - Monitoreo Red IP
# Script principal con detección inteligente de dependencias

param(
    [string]$command = "status"
)

function Show-Help {
    Write-Host "Sistema de Gestión - Monitoreo Red IP" -ForegroundColor Cyan
    Write-Host "======================================" -ForegroundColor Cyan
    Write-Host "Uso: .\manage-db.ps1 <comando>`n" -ForegroundColor Yellow
    
    Write-Host "Comandos disponibles:" -ForegroundColor Green
    Write-Host "  start           - Iniciar servicios con verificación inteligente" -ForegroundColor White
    Write-Host "  safe-shutdown   - Apagar con backup y preservar dependencias" -ForegroundColor White
    Write-Host "  restart         - Reiniciar servicios" -ForegroundColor White
    Write-Host "  backup          - Crear backup manual" -ForegroundColor White
    Write-Host "  restore         - Restaurar último backup" -ForegroundColor White
    Write-Host "  status          - Estado de servicios" -ForegroundColor White
    Write-Host "  list-backups    - Listar backups disponibles" -ForegroundColor White
    Write-Host "  logs            - Ver logs en tiempo real" -ForegroundColor White
    Write-Host "  setup-pgadmin   - Configurar PgAdmin persistente" -ForegroundColor White
    Write-Host "  force-install-deps - Forzar reinstalación de dependencias" -ForegroundColor White
    Write-Host "  force-init-auth - Forzar reinicialización datos auth" -ForegroundColor White
}

function Test-Dependencies {
    Write-Host "🔍 Verificando dependencias del backend..." -ForegroundColor Cyan
    try {
        $checkScript = @"
import sys
dependencies = ['fastapi', 'sqlalchemy', 'psycopg2', 'jose', 'passlib']
missing = []
for dep in dependencies:
    try:
        __import__(dep)
    except ImportError:
        missing.append(dep)

if missing:
    print(f'MISSING:{",".join(missing)}')
else:
    print('OK')
"@
        
        $result = docker exec monitoreo_backend python -c $checkScript
        return $result
    }
    catch {
        return "ERROR:$_"
    }
}

function Install-Dependencies {
    Write-Host "📦 Instalando dependencias..." -ForegroundColor Yellow
    try {
        docker exec monitoreo_backend pip install --upgrade pip
        docker exec monitoreo_backend pip install -r /app/requirements.txt
        return $true
    }
    catch {
        Write-Host "❌ Error instalando dependencias: $_" -ForegroundColor Red
        return $false
    }
}

function Test-AuthData {
    Write-Host "🔍 Verificando datos de autenticación..." -ForegroundColor Cyan
    try {
        $userCount = docker exec monitoreo_postgres psql -U monitoreo_user -d monitoreo_dev -t -c "SELECT COUNT(*) FROM seguridad.usuario;" 2>$null
        if ($LASTEXITCODE -eq 0 -and $userCount -match '\d+') {
            return [int]$userCount
        }
        return 0
    }
    catch {
        return 0
    }
}

function Initialize-AuthData {
    Write-Host "🗃️ Inicializando datos de autenticación..." -ForegroundColor Yellow
    try {
        $sqlFile = ".\database\init-data\01-autenticacion-data.sql"
        if (Test-Path $sqlFile) {
            Get-Content $sqlFile | docker exec -i monitoreo_postgres psql -U monitoreo_user -d monitoreo_dev
            Write-Host "✅ Datos de autenticación inicializados" -ForegroundColor Green
            return $true
        }
        else {
            Write-Host "❌ Archivo de datos no encontrado: $sqlFile" -ForegroundColor Red
            return $false
        }
    }
    catch {
        Write-Host "❌ Error inicializando datos: $_" -ForegroundColor Red
        return $false
    }
}

# MENU PRINCIPAL
switch ($command) {
    "start" {
        Write-Host "🚀 Iniciando servicios con verificación inteligente..." -ForegroundColor Green
        
        # Iniciar servicios
        docker-compose up -d
        
        # Esperar que servicios estén listos
        Write-Host "⏳ Esperando que servicios estén listos..." -ForegroundColor Yellow
        Start-Sleep -Seconds 15
        
        # VERIFICACIÓN INTELIGENTE DE DEPENDENCIAS
        $depsResult = Test-Dependencies
        if ($depsResult -eq "OK") {
            Write-Host "✅ Todas las dependencias están instaladas" -ForegroundColor Green
        }
        elseif ($depsResult -like "MISSING:*") {
            Write-Host "⚠️  Faltan dependencias: $($depsResult.Replace('MISSING:',''))" -ForegroundColor Yellow
            if (Install-Dependencies) {
                Write-Host "✅ Dependencias instaladas correctamente" -ForegroundColor Green
            }
        }
        else {
            Write-Host "⚠️  No se pudo verificar dependencias, instalando preventivamente..." -ForegroundColor Yellow
            Install-Dependencies
        }
        
        # VERIFICACIÓN INTELIGENTE DE DATOS DE AUTENTICACIÓN
        $userCount = Test-AuthData
        if ($userCount -gt 0) {
            Write-Host "✅ Datos de autenticación existen ($userCount usuarios)" -ForegroundColor Green
        }
        else {
            Write-Host "⚠️  No hay datos de autenticación, inicializando..." -ForegroundColor Yellow
            Initialize-AuthData
        }
        
        Write-Host "`n🎉 Todos los servicios iniciados y configurados" -ForegroundColor Green
        docker-compose ps
    }
    
    "safe-shutdown" {
        Write-Host "🛑 Apagado seguro de servicios..." -ForegroundColor Yellow
        
        # Crear backup antes de apagar
        Write-Host "💾 Creando backup de base de datos..." -ForegroundColor Cyan
        $backupResult = .\scripts\backup-db.ps1
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ Backup creado correctamente" -ForegroundColor Green
        }
        else {
            Write-Host "⚠️  Backup falló, pero continuando con apagado..." -ForegroundColor Yellow
        }
        
        # Detener servicios (las dependencias persisten en el volumen)
        docker-compose down
        
        Write-Host "✅ Servicios apagados correctamente" -ForegroundColor Green
        Write-Host "📦 Dependencias preservadas en volumen Docker" -ForegroundColor Cyan
        Write-Host "💾 Backup de BD guardado en ./database/backups/" -ForegroundColor Cyan
    }
    
    "restart" {
        Write-Host "🔄 Reiniciando servicios..." -ForegroundColor Yellow
        docker-compose restart
        Write-Host "✅ Servicios reiniciados" -ForegroundColor Green
    }
    
    "backup" {
        Write-Host "💾 Creando backup manual..." -ForegroundColor Cyan
        .\scripts\backup-db.ps1
    }
    
    "restore" {
        Write-Host "🔄 Restaurando último backup..." -ForegroundColor Cyan
        .\scripts\restore-db.ps1
    }
    
    "status" {
        Write-Host "📊 Estado de los servicios:" -ForegroundColor Cyan
        docker-compose ps
        
        # Información adicional
        Write-Host "`n🔍 Información adicional:" -ForegroundColor Cyan
        try {
            $userCount = Test-AuthData
            Write-Host "   Usuarios en sistema: $userCount" -ForegroundColor White
            
            $depsResult = Test-Dependencies
            if ($depsResult -eq "OK") {
                Write-Host "   Dependencias: ✅ Todas instaladas" -ForegroundColor Green
            }
            else {
                Write-Host "   Dependencias: ⚠️  Verificar instalación" -ForegroundColor Yellow
            }
        }
        catch {
            Write-Host "   No se pudo obtener información adicional" -ForegroundColor Red
        }
    }
    
    "list-backups" {
        Write-Host "📂 Backups disponibles:" -ForegroundColor Cyan
        if (Test-Path ".\database\backups") {
            Get-ChildItem ".\database\backups" -Filter "*.backup" | Sort-Object LastWriteTime -Descending | Format-Table Name, LastWriteTime, Length -AutoSize
        }
        else {
            Write-Host "No hay backups disponibles" -ForegroundColor Yellow
        }
    }
    
    "logs" {
        Write-Host "📋 Mostrando logs en tiempo real (Ctrl+C para salir)..." -ForegroundColor Cyan
        docker-compose logs -f
    }
    
    "setup-pgadmin" {
        Write-Host "⚙️ Configurando PgAdmin persistente..." -ForegroundColor Cyan
        if (Test-Path ".\database\pgadmin-servers.json") {
            Write-Host "✅ Configuración de PgAdmin ya existe" -ForegroundColor Green
        }
        else {
            Write-Host "❌ Archivo de configuración no encontrado" -ForegroundColor Red
        }
    }
    
    "force-install-deps" {
        Write-Host "🔨 Forzando reinstalación de dependencias..." -ForegroundColor Cyan
        if (Install-Dependencies) {
            Write-Host "✅ Dependencias reinstaladas forzosamente" -ForegroundColor Green
        }
    }
    
    "force-init-auth" {
        Write-Host "🔨 Forzando reinicialización de datos de autenticación..." -ForegroundColor Cyan
        if (Initialize-AuthData) {
            Write-Host "✅ Datos de autenticación reinicializados" -ForegroundColor Green
        }
    }
    
    default {
        Write-Host "❌ Comando '$command' no reconocido`n" -ForegroundColor Red
        Show-Help
    }
}