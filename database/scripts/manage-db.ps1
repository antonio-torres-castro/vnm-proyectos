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
    Write-Host "  fix-pgadmin     - Solucionar problemas de permisos de pgAdmin" -ForegroundColor White
    Write-Host "  clean-pgadmin   - Limpiar datos de pgAdmin y empezar de nuevo" -ForegroundColor White
    Write-Host "  force-install-deps - Forzar reinstalación de dependencias" -ForegroundColor White
    Write-Host "  force-init-auth - Forzar reinicialización datos auth" -ForegroundColor White
    Write-Host "  init-monitoreo  - Crear tablas del esquema de monitoreo" -ForegroundColor White
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
psycopg2==2.9.11
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

function Initialize-MonitoreoData {
    Write-Host "Inicializando tablas de monitoreo..." -ForegroundColor Yellow
    try {
        # Verificar que existe el archivo de creación de tablas
        $monitoreoFile = "Tablas\CreacionTablasMonitoreo.sql"
        
        if (-not (Test-Path $monitoreoFile)) {
            Write-Host "Archivo de tablas de monitoreo no encontrado: $monitoreoFile" -ForegroundColor Red
            return $false
        }
        
        # Ejecutar script de creación de tablas de monitoreo
        Write-Host "Creando esquema y tablas de monitoreo..." -ForegroundColor Cyan
        Get-Content $monitoreoFile | docker exec -i monitoreo_postgres psql -U monitoreo_user -d monitoreo_dev
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "Tablas de monitoreo creadas exitosamente" -ForegroundColor Green
            return $true
        } else {
            Write-Host "Error ejecutando script de monitoreo" -ForegroundColor Red
            return $false
        }
    }
    catch {
        Write-Host "Error inicializando tablas de monitoreo: $($_.Exception.Message)" -ForegroundColor Red
        return $false
    }
}

function Test-MonitoreoData {
    Write-Host "Verificando tablas de monitoreo..." -ForegroundColor Cyan
    try {
        $tableCount = docker exec monitoreo_postgres psql -U monitoreo_user -d monitoreo_dev -t -c "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema='monitoreo';" 2>$null
        if ($LASTEXITCODE -eq 0 -and $tableCount -match '\d+') {
            return [int]$tableCount
        }
        return 0
    }
    catch {
        return 0
    }
}

function Fix-PgAdmin {
    Write-Host "Solucionando problemas de permisos de pgAdmin..." -ForegroundColor Yellow
    try {
        # Verificar si pgAdmin está corriendo
        $pgadminRunning = docker ps --filter "name=monitoreo_pgadmin" --filter "status=running" --format "{{.Names}}"
        
        if ($pgadminRunning) {
            Write-Host "Deteniendo contenedor pgAdmin..." -ForegroundColor Cyan
            docker stop monitoreo_pgadmin
            docker rm monitoreo_pgadmin
        }
        
        # Si existe el directorio de bind mount local, respaldarlo y eliminarlo
        $pgadminDataPath = "..\pgadmin-data"
        if (Test-Path $pgadminDataPath) {
            Write-Host "Respaldando configuración local de pgAdmin..." -ForegroundColor Cyan
            $backupPath = "..\pgadmin-data-backup-$(Get-Date -Format 'yyyyMMdd_HHmmss')"
            Copy-Item -Recurse $pgadminDataPath $backupPath -ErrorAction SilentlyContinue
            Write-Host "Backup creado en: $backupPath" -ForegroundColor Green
            
            Write-Host "Eliminando directorio problemático..." -ForegroundColor Cyan
            Remove-Item -Recurse -Force $pgadminDataPath -ErrorAction SilentlyContinue
        }
        
        # Reiniciar solo el servicio pgAdmin (ahora usará el volumen nombrado)
        Write-Host "Reiniciando pgAdmin con volumen nombrado..." -ForegroundColor Cyan
        docker-compose up -d pgadmin
        
        # Esperar a que pgAdmin esté listo
        Write-Host "Esperando a que pgAdmin esté listo..." -ForegroundColor Yellow
        Start-Sleep -Seconds 15
        
        # Verificar estado
        $status = docker ps --filter "name=monitoreo_pgadmin" --format "{{.Status}}"
        if ($status -match "Up") {
            Write-Host "pgAdmin solucionado y funcionando correctamente" -ForegroundColor Green
            Write-Host "Acceso: http://localhost:8081" -ForegroundColor Cyan
            Write-Host "Email: admin@monitoreo.cl" -ForegroundColor Cyan
            Write-Host "Password: admin123" -ForegroundColor Cyan
        } else {
            Write-Host "pgAdmin aún tiene problemas. Revisar logs: docker logs monitoreo_pgadmin" -ForegroundColor Red
        }
        
        return $true
    }
    catch {
        Write-Host "Error solucionando pgAdmin: $($_.Exception.Message)" -ForegroundColor Red
        return $false
    }
}

function Clean-PgAdmin {
    Write-Host "Limpiando completamente pgAdmin..." -ForegroundColor Yellow
    try {
        # Detener y eliminar contenedor
        Write-Host "Deteniendo contenedor pgAdmin..." -ForegroundColor Cyan
        docker stop monitoreo_pgadmin -ErrorAction SilentlyContinue
        docker rm monitoreo_pgadmin -ErrorAction SilentlyContinue
        
        # Eliminar volumen nombrado
        Write-Host "Eliminando volumen de datos de pgAdmin..." -ForegroundColor Cyan
        docker volume rm vnm-proyectos_pgadmin_data -ErrorAction SilentlyContinue
        
        # Eliminar directorio local si existe
        $pgadminDataPath = "..\pgadmin-data"
        if (Test-Path $pgadminDataPath) {
            Write-Host "Eliminando directorio local..." -ForegroundColor Cyan
            Remove-Item -Recurse -Force $pgadminDataPath -ErrorAction SilentlyContinue
        }
        
        # Recrear pgAdmin limpio
        Write-Host "Recreando pgAdmin limpio..." -ForegroundColor Cyan
        docker-compose up -d pgadmin
        
        Write-Host "pgAdmin limpiado y recreado completamente" -ForegroundColor Green
        Write-Host "Configuración inicial requerida en http://localhost:8081" -ForegroundColor Cyan
        
        return $true
    }
    catch {
        Write-Host "Error limpiando pgAdmin: $($_.Exception.Message)" -ForegroundColor Red
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
        
        # VERIFICACIÓN INTELIGENTE DE TABLAS DE MONITOREO
        $monitoreoTableCount = Test-MonitoreoData
        if ($monitoreoTableCount -ge 4) {
            Write-Host "Tablas de monitoreo existen ($monitoreoTableCount tablas)" -ForegroundColor Green
        }
        else {
            Write-Host "Tablas de monitoreo no encontradas, inicializando..." -ForegroundColor Yellow
            Initialize-MonitoreoData
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
    
    "fix-pgadmin" {
        Write-Host "Ejecutando reparación de pgAdmin..." -ForegroundColor Cyan
        if (Fix-PgAdmin) {
            Write-Host "Reparación de pgAdmin completada exitosamente" -ForegroundColor Green
        } else {
            Write-Host "La reparación de pgAdmin falló" -ForegroundColor Red
        }
    }
    
    "clean-pgadmin" {
        Write-Host "Ejecutando limpieza completa de pgAdmin..." -ForegroundColor Cyan
        if (Clean-PgAdmin) {
            Write-Host "Limpieza de pgAdmin completada exitosamente" -ForegroundColor Green
        } else {
            Write-Host "La limpieza de pgAdmin falló" -ForegroundColor Red
        }
    }
    
    "init-monitoreo" {
        Write-Host "Inicializando tablas de monitoreo..." -ForegroundColor Cyan
        if (Initialize-MonitoreoData) {
            Write-Host "Tablas de monitoreo inicializadas exitosamente" -ForegroundColor Green
        } else {
            Write-Host "La inicialización de tablas de monitoreo falló" -ForegroundColor Red
        }
    }
    
    default {
        Write-Host "Comando '$command' no reconocido`n" -ForegroundColor Red
        Show-Help
    }
}