#!/usr/bin/env pwsh

Write-Host "=== FORMATEO AUTOMATICO DE CODIGO PYTHON ===" -ForegroundColor Green
Write-Host "Aplicando Black formatter al codigo del backend..." -ForegroundColor Cyan
Write-Host ""

# Verificar si estamos en el directorio correcto
if (-not (Test-Path "backend")) {
    Write-Host " Error: No se encuentra el directorio 'backend'" -ForegroundColor Red
    Write-Host "Asegurate de ejecutar este script desde el directorio raiz del proyecto" -ForegroundColor Yellow
    exit 1
}

# Verificar si Black esta instalado
Write-Host "1. Verificando Black formatter..." -ForegroundColor Yellow
$blackVersion = python -m black --version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host " Black no esta instalado. Instalando..." -ForegroundColor Red
    python -m pip install black isort
    if ($LASTEXITCODE -ne 0) {
        Write-Host " Error instalando Black" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host " Black esta disponible: $blackVersion" -ForegroundColor Green
}

Write-Host ""

# Formatear con Black
Write-Host "2. Aplicando Black formatter..." -ForegroundColor Yellow
Write-Host "Formateando archivos Python en el backend..." -ForegroundColor Cyan

python -m black backend/ --line-length=88 --target-version=py311 --diff
if ($LASTEXITCODE -eq 0) {
    Write-Host " Previsualizacion completada. Aplicando cambios..." -ForegroundColor Green
    python -m black backend/ --line-length=88 --target-version=py311
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host " Formateo con Black completado" -ForegroundColor Green
    } else {
        Write-Host " Error aplicando Black" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host " Error verificando archivos con Black" -ForegroundColor Red
    exit 1
}

Write-Host ""

# Organizar imports con isort
Write-Host "3. Organizando imports..." -ForegroundColor Yellow
$isortVersion = python -m isort --version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host " isort no esta instalado. Instalando..." -ForegroundColor Red
    python -m pip install isort
}

python -m isort backend/ --profile=black --diff
if ($LASTEXITCODE -eq 0) {
    Write-Host " Previsualizacion de imports completada. Aplicando cambios..." -ForegroundColor Green
    python -m isort backend/ --profile=black
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host " Organizacion de imports completada" -ForegroundColor Green
    } else {
        Write-Host " Error organizando imports" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host " Error verificando imports" -ForegroundColor Red
    exit 1
}

Write-Host ""

# Verificar con flake8
Write-Host "4. Verificando con flake8..." -ForegroundColor Yellow
$flake8Version = python -m flake8 --version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host " flake8 no esta instalado. Instalando..." -ForegroundColor Red
    python -m pip install flake8
}

python -m flake8 backend/ --max-line-length=88 --extend-ignore=E203,W503 --statistics
if ($LASTEXITCODE -eq 0) {
    Write-Host " Verificacion con flake8 completada - Sin errores" -ForegroundColor Green
} else {
    Write-Host "  Verificacion con flake8 completada - Revisar advertencias arriba" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "=== FORMATEO COMPLETADO ===" -ForegroundColor Green
Write-Host ""
Write-Host " RESUMEN:" -ForegroundColor Cyan
Write-Host " Codigo formateado con Black (líneas max: 88 caracteres)" -ForegroundColor White
Write-Host " Imports organizados con isort" -ForegroundColor White
Write-Host " Verificacion con flake8 completada" -ForegroundColor White
Write-Host ""
Write-Host " CONFIGURACION VS CODE:" -ForegroundColor Cyan
Write-Host "- Formateo automatico al guardar: HABILITADO" -ForegroundColor White
Write-Host "- Linting con flake8: HABILITADO" -ForegroundColor White
Write-Host "- Limite visual de linea: 88 caracteres" -ForegroundColor White
Write-Host ""
Write-Host " PROXIMOS PASOS:" -ForegroundColor Cyan
Write-Host "1. Reinicia VS Code para aplicar la nueva configuracion" -ForegroundColor White
Write-Host "2. Los archivos ahora se formatearan automaticamente al guardar" -ForegroundColor White
Write-Host "3. El linting mostrara advertencias solo para problemas reales" -ForegroundColor White