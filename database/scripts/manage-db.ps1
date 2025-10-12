# Sistema de Gestión de Base de Datos - Monitoreo Red IP
# Script principal con detección inteligente y reparación automática

param(
    [string]$command = "status"
)

function Show-Help {
    Write-Host "Sistema de Gestión - Monitoreo Red IP" -ForegroundColor Cyan
    Write-Host "======================================" -ForegroundColor Cyan
    Write-Host "Uso: .\manage-db.ps1 <comando>`n" -ForegroundColor Yellow
    
    Write-Host "Comandos disponibles:" -ForegroundColor Green
    Write-Host "  start           - Iniciar servicios con verificación y reparación automática" -ForegroundColor White
    Write-Host "  safe-shutdown   - Apagar con backup y preservar dependencias" -ForegroundColor White
    Write-Host "  restart         - Reiniciar servicios" -ForegroundColor White
    Write-Host "  backup          - Crear backup manual" -ForegroundColor White
    Write-Host "  restore         - Restaurar último backup" -ForegroundColor White
    Write-Host "  status          - Estado de servicios con info de dependencias" -ForegroundColor White
    Write-Host "  repair-dependencies - Reparación completa de dependencias" -ForegroundColor White
    Write-Host "  list-backups    - Listar backups disponibles" -ForegroundColor White
    Write-Host "  logs            - Ver logs en tiempo real" -ForegroundColor White
    Write-Host "  setup-pgadmin   - Configurar PgAdmin persistente" -ForegroundColor White
    Write-Host "  force-install-deps - Forzar reinstalación de dependencias" -ForegroundColor White
    Write-Host "  force-init-auth - Forzar reinicialización datos auth" -ForegroundColor White
}

function Test-Dependencies {
    Write-Host "Verificando dependencias del backend..." -ForegroundColor Cyan
    try {
        # Definimos el script Python en una sola línea, para evitar errores de comillas o saltos de línea
        $checkScript = @"
import sys
deps=["fastapi","sqlalchemy","psycopg2","jose","passlib","email_validator","pydantic","uvicorn","python-multipart"]
missing=[]
for d in deps:
    try:
        __import__(d)
    except ImportError:
        missing.append(d)
print("OK" if not missing else "MISSING:" + ",".join(missing))
"@

        # Guardar el script en un archivo temporal dentro del contenedor (más robusto que -c)
        $tempFile = "/tmp/check_deps.py"

        # Copiamos el script al contenedor Docker
        $checkScript | Set-Content -Encoding utf8 check_deps.py
        docker cp check_deps.py monitoreo_backend:$tempFile | Out-Null

        # Ejecutamos el script dentro del contenedor
        $result = docker exec monitoreo_backend python $tempFile

        # Eliminamos el archivo temporal local
        Remove-Item check_deps.py -ErrorAction SilentlyContinue

        return $result
    }
    catch {
        return "ERROR: $($_.Exception.Message)"
    }
}


function Install-Dependencies {
    Write-Host "Instalando/Actualizando dependencias..." -ForegroundColor Yellow
    try {
        # Actualizar requirements.txt en el contenedor primero
        $updatedRequirements = @"
fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlalchemy==2.0.23
psycopg2-binary==2.9.9
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
pydantic[email]==2.5.0
python-dotenv==1.0.0
email-validator==2.0.0
python-multipart==0.0.6
"@
        
        # Actualizar el archivo requirements.txt en el contenedor
        $updatedRequirements | docker exec -i monitoreo_backend tee /app/requirements.txt > $null
        
        # Instalar dependencias suprimiendo warnings de root
        docker exec monitoreo_backend pip install --root-user-action=ignore --upgrade pip
        docker exec monitoreo_backend pip install --root-user-action=ignore --force-reinstall -r /app/requirements.txt
        
        Write-Host "Dependencias instaladas/actualizadas correctamente" -ForegroundColor Green
        return $true
    }
    catch {
        Write-Host "Error instalando dependencias: $($_.Exception.Message)" -ForegroundColor Red
        return $false
    }
}

function Test-AuthData {
    Write-Host "Verificando datos de autenticación..." -ForegroundColor Cyan
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
    Write-Host "Inicializando datos de autenticación..." -ForegroundColor Yellow
    try {
        # Primero verificar que existen los archivos de inicialización
        $schemaFile = "..\init-data\01-esquema-seguridad.sql"
        $dataFile = "..\init-data\02-datos-autenticacion.sql"
        
        if (-not (Test-Path $schemaFile)) {
            Write-Host "Archivo de esquema no encontrado: $schemaFile" -ForegroundColor Red
            return $false
        }
        
        if (-not (Test-Path $dataFile)) {
            Write-Host "Archivo de datos no encontrado: $dataFile" -ForegroundColor Red
            return $false
        }
        
        # Ejecutar esquema primero, luego datos
        Write-Host "Creando esquema de seguridad..." -ForegroundColor Cyan
        Get-Content $schemaFile | docker exec -i monitoreo_postgres psql -U monitoreo_user -d monitoreo_dev
        
        Write-Host "Insertando datos iniciales..." -ForegroundColor Cyan
        Get-Content $dataFile | docker exec -i monitoreo_postgres psql -U monitoreo_user -d monitoreo_dev
        
        Write-Host "Datos de autenticación inicializados" -ForegroundColor Green
        return $true
    }
    catch {
        Write-Host "Error inicializando datos: $($_.Exception.Message)" -ForegroundColor Red
        return $false
    }
}

# MENU PRINCIPAL
switch ($command) {
    "start" {
        Write-Host "Iniciando servicios con verificación inteligente..." -ForegroundColor Green
        
        # Iniciar servicios
        docker-compose up -d
        
        # Esperar que servicios estén listos
        Write-Host "Esperando que servicios estén listos..." -ForegroundColor Yellow
        Start-Sleep -Seconds 20
        
        # VERIFICACIÓN Y REPARACIÓN AUTOMÁTICA DE DEPENDENCIAS
        Write-Host "Verificando estado de dependencias críticas..." -ForegroundColor Cyan
        $depsResult = Test-Dependencies
        if ($depsResult -eq "OK") {
            Write-Host "Todas las dependencias están instaladas" -ForegroundColor Green
        }
        else {
            Write-Host "Problemas detectados: $depsResult" -ForegroundColor Yellow
            Write-Host "Ejecutando reparación automática..." -ForegroundColor Cyan
            if (Install-Dependencies) {
                Write-Host "Reparación completada" -ForegroundColor Green
                # Reiniciar backend con nuevas dependencias
                docker-compose restart backend
                Start-Sleep -Seconds 5
            }
            else {
                Write-Host "No se pudo completar la reparación automática" -ForegroundColor Red
            }
        }
        
        # VERIFICACIÓN INTELIGENTE DE DATOS DE AUTENTICACIÓN
        $userCount = Test-AuthData
        if ($userCount -gt 0) {
            Write-Host "Datos de autenticación existen ($userCount usuarios)" -ForegroundColor Green
        }
        else {
            Write-Host "No hay datos de autenticación, inicializando..." -ForegroundColor Yellow
            Initialize-AuthData
        }
        
        Write-Host "`nTodos los servicios iniciados y configurados" -ForegroundColor Green
        docker-compose ps
    }
    
    "safe-shutdown" {
        Write-Host "Apagado seguro de servicios..." -ForegroundColor Yellow
        
        # Crear backup antes de apagar
        Write-Host "Creando backup de base de datos..." -ForegroundColor Cyan
        $backupResult = .\backup-db.ps1
        if ($LASTEXITCODE -eq 0) {
            Write-Host "Backup creado correctamente" -ForegroundColor Green
        }
        else {
            Write-Host "Backup falló, pero continuando con apagado..." -ForegroundColor Yellow
        }
        
        # Detener servicios (las dependencias persisten en el volumen)
        docker-compose down
        
        Write-Host "Servicios apagados correctamente" -ForegroundColor Green
        Write-Host "Dependencias preservadas en volumen Docker" -ForegroundColor Cyan
        Write-Host "Backup de BD guardado en ../backups/" -ForegroundColor Cyan
    }
    
    "restart" {
        Write-Host "Reiniciando servicios..." -ForegroundColor Yellow
        docker-compose restart
        Write-Host "Servicios reiniciados" -ForegroundColor Green
    }
    
    "backup" {
        Write-Host "Creando backup manual..." -ForegroundColor Cyan
        .\backup-db.ps1
    }
    
    "restore" {
        Write-Host "Restaurando último backup..." -ForegroundColor Cyan
        .\restore-db.ps1
    }
    
    "status" {
        Write-Host "Estado de los servicios:" -ForegroundColor Cyan
        docker-compose ps
        
        # Información adicional
        Write-Host "`nInformación adicional:" -ForegroundColor Cyan
        try {
            $userCount = Test-AuthData
            Write-Host "   Usuarios en sistema: $userCount" -ForegroundColor White
            
            $depsResult = Test-Dependencies
            if ($depsResult -eq "OK") {
                Write-Host "   Dependencias: Todas instaladas" -ForegroundColor Green
            }
            else {
                Write-Host "   Dependencias: $depsResult" -ForegroundColor Yellow
            }
        }
        catch {
            Write-Host "   No se pudo obtener información adicional" -ForegroundColor Red
        }
    }
    
    "repair-dependencies" {
        Write-Host "Ejecutando reparación completa de dependencias..." -ForegroundColor Cyan
        if (Install-Dependencies) {
            Write-Host "Reparación completada - Reiniciando backend..." -ForegroundColor Green
            docker-compose restart backend
            Write-Host "Backend reiniciado con nuevas dependencias" -ForegroundColor Green
        }
        else {
            Write-Host "Reparación falló" -ForegroundColor Red
        }
    }
    
    "list-backups" {
        Write-Host "Backups disponibles:" -ForegroundColor Cyan
        if (Test-Path "..\backups") {
            Get-ChildItem "..\backups" -Filter "*.backup" | Sort-Object LastWriteTime -Descending | Format-Table Name, LastWriteTime, Length -AutoSize
        }
        else {
            Write-Host "No hay backups disponibles" -ForegroundColor Yellow
        }
    }
    
    "logs" {
        Write-Host "Mostrando logs en tiempo real (Ctrl+C para salir)..." -ForegroundColor Cyan
        docker-compose logs -f
    }
    
    "setup-pgadmin" {
        Write-Host "Configurando PgAdmin persistente..." -ForegroundColor Cyan
        if (Test-Path "..\pgadmin-servers.json") {
            Write-Host "Configuración de PgAdmin ya existe" -ForegroundColor Green
        }
        else {
            Write-Host "Archivo de configuración no encontrado" -ForegroundColor Red
        }
    }
    
    "force-install-deps" {
        Write-Host "Forzando reinstalación de dependencias..." -ForegroundColor Cyan
        if (Install-Dependencies) {
            Write-Host "Dependencias reinstaladas forzosamente" -ForegroundColor Green
        }
    }
    
    "force-init-auth" {
        Write-Host "Forzando reinicialización de datos de autenticación..." -ForegroundColor Cyan
        if (Initialize-AuthData) {
            Write-Host "Datos de autenticación reinicializados" -ForegroundColor Green
        }
    }
    
    default {
        Write-Host "Comando '$command' no reconocido`n" -ForegroundColor Red
        Show-Help
    }
}