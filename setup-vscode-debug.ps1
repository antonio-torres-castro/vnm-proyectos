#!/usr/bin/env pwsh
# Script de configuración para debugging en VS Code - Windows PowerShell

Write-Host "Configurando entorno de debugging de VS Code..." -ForegroundColor Green

# Función para crear directorio si no existe
function Create-Directory-If-Not-Exists($path) {
    if (!(Test-Path -Path $path)) {
        New-Item -ItemType Directory -Path $path -Force | Out-Null
        Write-Host "Creado directorio: $path" -ForegroundColor Yellow
    }
}

# Función para copiar archivos con verificación
function Copy-With-Verification($source, $destination) {
    if (Test-Path -Path $source) {
        Copy-Item -Path $source -Destination $destination -Force
        Write-Host "Copiado: $source -> $destination" -ForegroundColor Green
    } else {
        Write-Host "Archivo fuente no encontrado: $source" -ForegroundColor Red
    }
}

try {
    # Verificar que estamos en el directorio correcto
    if (!(Test-Path -Path "vscode-config")) {
        Write-Host "Error: Directorio 'vscode-config' no encontrado" -ForegroundColor Red
        Write-Host "Asegúrate de ejecutar este script desde la raíz del proyecto vnm-proyectos" -ForegroundColor Red
        exit 1
    }

    # Crear directorios .vscode
    Write-Host "Creando directorios .vscode..." -ForegroundColor Cyan
    Create-Directory-If-Not-Exists ".vscode"
    Create-Directory-If-Not-Exists "backend\.vscode"
    Create-Directory-If-Not-Exists "frontend\.vscode"

    # Copiar configuraciones del directorio raíz
    Write-Host "Copiando configuraciones del directorio raíz..." -ForegroundColor Cyan
    Copy-With-Verification "vscode-config\root\launch.json" ".vscode\launch.json"
    Copy-With-Verification "vscode-config\root\tasks.json" ".vscode\tasks.json"
    Copy-With-Verification "vscode-config\root\extensions.json" ".vscode\extensions.json"
    Copy-With-Verification "vscode-config\root\settings.json" ".vscode\settings.json"

    # Copiar configuraciones del backend
    Write-Host "Copiando configuraciones del backend..." -ForegroundColor Cyan
    Copy-With-Verification "vscode-config\backend\launch.json" "backend\.vscode\launch.json"
    Copy-With-Verification "vscode-config\backend\settings.json" "backend\.vscode\settings.json"

    # Copiar configuraciones del frontend
    Write-Host "Copiando configuraciones del frontend..." -ForegroundColor Cyan
    Copy-With-Verification "vscode-config\frontend\launch.json" "frontend\.vscode\launch.json"
    Copy-With-Verification "vscode-config\frontend\extensions.json" "frontend\.vscode\extensions.json"

    Write-Host ""
    Write-Host "¡Configuración completada exitosamente!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Próximos pasos:" -ForegroundColor Yellow
    Write-Host "1. Abrir VS Code: code ." -ForegroundColor White
    Write-Host "2. Instalar extensiones recomendadas cuando VS Code lo sugiera" -ForegroundColor White
    Write-Host "3. Ejecutar task 'Debug: Full Environment Setup' para iniciar todo" -ForegroundColor White
    Write-Host ""

} catch {
    Write-Host "Error durante la configuración: $_" -ForegroundColor Red
    exit 1
}
