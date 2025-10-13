# PowerShell Script para configurar debugging de VS Code
# Ejecutar desde la raíz del proyecto vnm-proyectos

Write-Host "Configurando entorno de debugging de VS Code..." -ForegroundColor Green

# Crear directorios .vscode si no existen
$directories = @(
    ".vscode",
    "backend\.vscode", 
    "frontend\.vscode"
)

foreach ($dir in $directories) {
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
        Write-Host "Creado: $dir" -ForegroundColor Green
    }
    else {
        Write-Host "Ya existe: $dir" -ForegroundColor Yellow
    }
}

# Copiar configuraciones desde vscode-config a .vscode
$copies = @(
    @{Source = "vscode-config\root\*"; Destination = ".vscode\" },
    @{Source = "vscode-config\backend\*"; Destination = "backend\.vscode\" },
    @{Source = "vscode-config\frontend\*"; Destination = "frontend\.vscode\" }
)

foreach ($copy in $copies) {
    try {
        Copy-Item -Path $copy.Source -Destination $copy.Destination -Force -Recurse
        Write-Host "Copiado: $($copy.Source) -> $($copy.Destination)" -ForegroundColor Green
    }
    catch {
        Write-Host "Error copiando: $($copy.Source)" -ForegroundColor Red
        Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
    }
}

# Verificar que los archivos se copiaron correctamente
$requiredFiles = @(
    ".vscode\launch.json",
    ".vscode\tasks.json", 
    ".vscode\settings.json",
    ".vscode\extensions.json",
    "backend\.vscode\launch.json",
    "backend\.vscode\settings.json",
    "frontend\.vscode\launch.json",
    "frontend\.vscode\settings.json"
)

Write-Host "Verificando configuraciones..." -ForegroundColor Cyan
$allExists = $true

foreach ($file in $requiredFiles) {
    if (Test-Path $file) {
        Write-Host "$file" -ForegroundColor Green
    }
    else {
        Write-Host "$file" -ForegroundColor Red
        $allExists = $false
    }
}

if ($allExists) {
    Write-Host "Configuración de debugging completada exitosamente!" -ForegroundColor Green
    Write-Host "Revisa DEBUG_SETUP.md para instrucciones de uso" -ForegroundColor Cyan
    Write-Host "Próximos pasos:" -ForegroundColor Yellow
    Write-Host "1. Abrir VS Code en esta carpeta: code ." -ForegroundColor White
    Write-Host "2. Instalar extensiones recomendadas" -ForegroundColor White
    Write-Host "3. Iniciar Docker: docker-compose -f docker-compose.debug.yml up -d" -ForegroundColor White
    Write-Host "4. Arreglar login: Ctrl+Shift+P -> Tasks: Run Task -> Fix Admin Password" -ForegroundColor White
    Write-Host "5. Debuggear: Ctrl+Shift+D -> 🚀 Full Stack: Debug Both -> F5" -ForegroundColor White
}
else {
    Write-Host "Algunos archivos no se copiaron correctamente" -ForegroundColor Red
    Write-Host "Revisa los permisos y vuelve a ejecutar el script" -ForegroundColor Yellow
}

Write-Host "Configuraciones disponibles:" -ForegroundColor Cyan
Write-Host "Full Stack: Debug Both - Debuggea backend + frontend" -ForegroundColor White
Write-Host "Backend: FastAPI Docker Debug - Solo backend" -ForegroundColor White  
Write-Host "Frontend: React Chrome Debug - Solo frontend" -ForegroundColor White
Write-Host "Tests con debugging para ambos proyectos" -ForegroundColor White
