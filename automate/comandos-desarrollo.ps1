# Comandos rápidos para desarrollo VNM-Proyectos (Windows PowerShell)
# Uso: .\comandos-desarrollo.ps1 [comando]
# O cargar funciones: . .\comandos-desarrollo.ps1

param(
    [string]$Command = ""
)

# Función para mostrar texto con colores
function Write-ColorText {
    param(
        [string]$Text,
        [string]$Color = "White"
    )
    Write-Host $Text -ForegroundColor $Color
}

# Función para mostrar comandos disponibles
function Show-DevHelp {
    Write-Host ""
    Write-ColorText "║║║║║║║║║║║║║║║║║║║║║║║║║║║║║║║║║║║║║║║║║║║║║║║║║║║║║║║║║║║" "Cyan"
    Write-ColorText "║  🚀 Comandos de Desarrollo VNM-Proyectos (PowerShell)  ║" "Cyan"
    Write-ColorText "║║║║║║║║║║║║║║║║║║║║║║║║║║║║║║║║║║║║║║║║║║║║║║║║║║║║║║║║║║║" "Cyan"
    Write-Host ""
    Write-ColorText "📋 COMANDOS PRINCIPALES:" "Green"
    Write-ColorText "  Dev-Start            - Iniciar entorno de desarrollo" "Yellow"
    Write-ColorText "  Dev-Start-Rebuild    - Iniciar con rebuild de Docker" "Yellow"
    Write-ColorText "  Dev-Start-PgAdmin    - Iniciar con PgAdmin incluido" "Yellow"
    Write-ColorText "  Dev-Status           - Verificar estado del entorno" "Yellow"
    Write-ColorText "  Dev-Stop             - Parar entorno (con backup)" "Yellow"
    Write-ColorText "  Dev-Stop-Clean       - Parar y limpiar completamente" "Yellow"
    Write-ColorText "  Dev-Restart          - Regenerar entorno completo" "Yellow"
    Write-ColorText "  Dev-Backup           - Crear backup manual" "Yellow"
    Write-Host ""
    Write-ColorText "🔍 MONITOREO:" "Green"
    Write-ColorText "  Dev-Logs             - Ver logs de todos los servicios" "Yellow"
    Write-ColorText "  Dev-Logs-Backend     - Ver logs solo del backend" "Yellow"
    Write-ColorText "  Dev-Logs-DB          - Ver logs solo de PostgreSQL" "Yellow"
    Write-ColorText "  Dev-PS               - Ver contenedores activos" "Yellow"
    Write-ColorText "  Dev-Health           - Verificar salud de servicios" "Yellow"
    Write-Host ""
    Write-ColorText "🛠️ TROUBLESHOOTING:" "Green"
    Write-ColorText "  Dev-Clean-Docker     - Limpiar recursos Docker no utilizados" "Yellow"
    Write-ColorText "  Dev-Reset            - Reset completo (PELIGROSO)" "Yellow"
    Write-Host ""
    Write-ColorText "🌐 ABRIR URLs:" "Green"
    Write-ColorText "  Dev-Open api         - Abrir Backend API" "Yellow"
    Write-ColorText "  Dev-Open docs        - Abrir API Docs" "Yellow"
    Write-ColorText "  Dev-Open frontend    - Abrir Frontend" "Yellow"
    Write-ColorText "  Dev-Open pgadmin     - Abrir PgAdmin" "Yellow"
    Write-Host ""
    Write-ColorText "🌐 URLs ÚTILES:" "Green"
    Write-Host "  Backend API:    " -NoNewline; Write-ColorText "http://localhost:8000" "Blue"
    Write-Host "  API Docs:       " -NoNewline; Write-ColorText "http://localhost:8000/docs" "Blue"
    Write-Host "  Frontend:       " -NoNewline; Write-ColorText "http://localhost:3000" "Blue"
    Write-Host "  PgAdmin:        " -NoNewline; Write-ColorText "http://localhost:5050" "Blue"; Write-Host " (admin@monitoreo.dev / admin123)"
    Write-Host ""
}

# 📋 COMANDOS PRINCIPALES

function Dev-Start {
    Write-ColorText "🚀 Iniciando entorno de desarrollo..." "Green"
    python devtools/orquestador_desarrollo.py iniciar
}

function Dev-Start-Rebuild {
    Write-ColorText "🚀 Iniciando con rebuild de imágenes Docker..." "Green"
    python devtools/orquestador_desarrollo.py iniciar --rebuild
}

function Dev-Start-PgAdmin {
    Write-ColorText "🚀 Iniciando entorno con PgAdmin..." "Green"
    docker-compose -f docker-compose.debug.yml --profile pgadmin up -d
}

function Dev-Status {
    Write-ColorText "🔍 Verificando estado del entorno..." "Blue"
    python devtools/orquestador_desarrollo.py diagnosticar
}

function Dev-Stop {
    Write-ColorText "⬇️ Parando entorno (con backup automático)..." "Yellow"
    python devtools/orquestador_desarrollo.py terminar
}

function Dev-Stop-Clean {
    Write-ColorText "🧹 Parando y limpiando completamente..." "Red"
    Write-ColorText "⚠️ ESTO ELIMINARÁ TODOS LOS DATOS DE DESARROLLO" "Red"
    $confirm = Read-Host "¿Estás seguro? (s/N)"
    if ($confirm -eq "s" -or $confirm -eq "S") {
        python devtools/orquestador_desarrollo.py terminar --limpiar-completo
    } else {
        Write-ColorText "Operación cancelada" "Yellow"
    }
}

function Dev-Restart {
    Write-ColorText "🔄 Regenerando entorno completo..." "Blue"
    python devtools/orquestador_desarrollo.py regenerar
}

function Dev-Backup {
    Write-ColorText "💾 Creando backup manual..." "Green"
    python devtools/orquestador_desarrollo.py backup
}

# 🔍 MONITOREO

function Dev-Logs {
    Write-ColorText "📋 Mostrando logs de todos los servicios..." "Blue"
    docker-compose -f docker-compose.debug.yml logs -f
}

function Dev-Logs-Backend {
    Write-ColorText "📋 Mostrando logs del backend..." "Blue"
    try {
        docker logs -f backend_debug
    } catch {
        Write-ColorText "Backend no está ejecutándose" "Red"
    }
}

function Dev-Logs-DB {
    Write-ColorText "📋 Mostrando logs de PostgreSQL..." "Blue"
    try {
        docker logs -f postgres_debug
    } catch {
        Write-ColorText "PostgreSQL no está ejecutándose" "Red"
    }
}

function Dev-PS {
    Write-ColorText "📦 Contenedores activos:" "Blue"
    docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
}

function Dev-Health {
    Write-ColorText "🏥 Verificando salud de servicios..." "Blue"
    Write-Host ""
    
    # Backend API
    try {
        $null = Invoke-WebRequest -Uri "http://localhost:8000/health" -UseBasicParsing -TimeoutSec 5
        Write-Host "  Backend API:    " -NoNewline; Write-ColorText "✅ Healthy" "Green"
    } catch {
        Write-Host "  Backend API:    " -NoNewline; Write-ColorText "❌ No responde" "Red"
    }
    
    # Frontend
    try {
        $null = Invoke-WebRequest -Uri "http://localhost:3000" -UseBasicParsing -TimeoutSec 5
        Write-Host "  Frontend:       " -NoNewline; Write-ColorText "✅ Accessible" "Green"
    } catch {
        Write-Host "  Frontend:       " -NoNewline; Write-ColorText "❌ No responde" "Red"
    }
    
    # PostgreSQL
    try {
        $null = docker exec postgres_debug pg_isready -U vnm_user 2>$null
        if ($LASTEXITCODE -eq 0) {
            Write-Host "  PostgreSQL:     " -NoNewline; Write-ColorText "✅ Ready" "Green"
        } else {
            Write-Host "  PostgreSQL:     " -NoNewline; Write-ColorText "❌ No disponible" "Red"
        }
    } catch {
        Write-Host "  PostgreSQL:     " -NoNewline; Write-ColorText "❌ No disponible" "Red"
    }
    
    # Redis
    try {
        $null = docker exec redis_debug redis-cli ping 2>$null
        if ($LASTEXITCODE -eq 0) {
            Write-Host "  Redis:          " -NoNewline; Write-ColorText "✅ Responding" "Green"
        } else {
            Write-Host "  Redis:          " -NoNewline; Write-ColorText "❌ No disponible" "Red"
        }
    } catch {
        Write-Host "  Redis:          " -NoNewline; Write-ColorText "❌ No disponible" "Red"
    }
}

# 🛠️ TROUBLESHOOTING

function Dev-Clean-Docker {
    Write-ColorText "🧹 Limpiando recursos Docker no utilizados..." "Yellow"
    docker system prune -f
    docker volume prune -f
}

function Dev-Reset {
    Write-ColorText "💥 RESET COMPLETO DEL ENTORNO" "Red"
    Write-ColorText "⚠️ ESTO ELIMINARÁ TODO: contenedores, volúmenes, imágenes" "Red"
    $confirm = Read-Host "¿Estás COMPLETAMENTE seguro? (escriba 'RESET' para confirmar)"
    if ($confirm -eq "RESET") {
        Write-ColorText "🔥 Ejecutando reset completo..." "Red"
        python devtools/orquestador_desarrollo.py terminar --limpiar-completo --sin-backup
        docker system prune -a -f
        docker volume prune -f
        Write-ColorText "✅ Reset completo terminado" "Green"
    } else {
        Write-ColorText "Operación cancelada" "Yellow"
    }
}

# 🌐 FUNCIONES ÚTILES

function Dev-Open {
    param([string]$Service)
    
    switch ($Service.ToLower()) {
        "api" { Start-Process "http://localhost:8000" }
        "backend" { Start-Process "http://localhost:8000" }
        "docs" { Start-Process "http://localhost:8000/docs" }
        "frontend" { Start-Process "http://localhost:3000" }
        "web" { Start-Process "http://localhost:3000" }
        "pgadmin" { Start-Process "http://localhost:5050" }
        "admin" { Start-Process "http://localhost:5050" }
        default { 
            Write-ColorText "Uso: Dev-Open {api|docs|frontend|pgadmin}" "Yellow"
        }
    }
}

# Aliases para compatibilidad
Set-Alias -Name dev-start -Value Dev-Start
Set-Alias -Name dev-status -Value Dev-Status
Set-Alias -Name dev-stop -Value Dev-Stop
Set-Alias -Name dev-logs -Value Dev-Logs
Set-Alias -Name dev-health -Value Dev-Health
Set-Alias -Name dev-help -Value Show-DevHelp

# Si se ejecuta con parámetros, ejecutar el comando correspondiente
if ($Command -ne "") {
    switch ($Command.ToLower()) {
        "help" { Show-DevHelp }
        "start" { Dev-Start }
        "start-rebuild" { Dev-Start-Rebuild }
        "start-pgadmin" { Dev-Start-PgAdmin }
        "status" { Dev-Status }
        "stop" { Dev-Stop }
        "stop-clean" { Dev-Stop-Clean }
        "restart" { Dev-Restart }
        "backup" { Dev-Backup }
        "logs" { Dev-Logs }
        "logs-backend" { Dev-Logs-Backend }
        "logs-db" { Dev-Logs-DB }
        "ps" { Dev-PS }
        "health" { Dev-Health }
        "clean-docker" { Dev-Clean-Docker }
        "reset" { Dev-Reset }
        default { 
            Write-ColorText "Comando no reconocido: $Command" "Red"
            Show-DevHelp
        }
    }
} else {
    # Si se carga como módulo sin parámetros, mostrar mensaje de bienvenida
    Write-ColorText "✅ Comandos de desarrollo cargados" "Green"
    Write-ColorText "Ejecuta 'Show-DevHelp' o 'dev-help' para ver todos los comandos disponibles" "White"
}
