@echo off
REM Comandos rápidos para desarrollo VNM-Proyectos (Windows Command Prompt)
REM Uso: comandos-desarrollo.bat [comando]

setlocal enabledelayedexpansion

REM Verificar si se pasó un comando como parámetro
if "%1"=="" goto show_help
if "%1"=="help" goto show_help
if "%1"=="start" goto dev_start
if "%1"=="start-rebuild" goto dev_start_rebuild
if "%1"=="start-pgadmin" goto dev_start_pgadmin
if "%1"=="status" goto dev_status
if "%1"=="stop" goto dev_stop
if "%1"=="stop-clean" goto dev_stop_clean
if "%1"=="restart" goto dev_restart
if "%1"=="backup" goto dev_backup
if "%1"=="logs" goto dev_logs
if "%1"=="logs-backend" goto dev_logs_backend
if "%1"=="logs-db" goto dev_logs_db
if "%1"=="ps" goto dev_ps
if "%1"=="health" goto dev_health
if "%1"=="clean-docker" goto dev_clean_docker
if "%1"=="reset" goto dev_reset
if "%1"=="open" goto dev_open

echo Comando no reconocido: %1
goto show_help

:show_help
echo.
echo ^|^|^|^|^|^|^|^|^|^|^|^|^|^|^|^|^|^|^|^|^|^|^|^|^|^|^|^|^|^|^|^|^|^|^|^|^|^|^|^|^|^|^|^|^|^|^|^|^|^|^|^|^|^|^|^|^|^|
echo ^|  🚀 Comandos de Desarrollo VNM-Proyectos (Windows)  ^|
echo ^|^|^|^|^|^|^|^|^|^|^|^|^|^|^|^|^|^|^|^|^|^|^|^|^|^|^|^|^|^|^|^|^|^|^|^|^|^|^|^|^|^|^|^|^|^|^|^|^|^|^|^|^|^|^|^|^|^|
echo.
echo 📋 COMANDOS PRINCIPALES:
echo   comandos-desarrollo.bat start            - Iniciar entorno de desarrollo
echo   comandos-desarrollo.bat start-rebuild    - Iniciar con rebuild de Docker
echo   comandos-desarrollo.bat start-pgadmin    - Iniciar con PgAdmin incluido
echo   comandos-desarrollo.bat status           - Verificar estado del entorno
echo   comandos-desarrollo.bat stop             - Parar entorno (con backup)
echo   comandos-desarrollo.bat stop-clean       - Parar y limpiar completamente
echo   comandos-desarrollo.bat restart          - Regenerar entorno completo
echo   comandos-desarrollo.bat backup           - Crear backup manual
echo.
echo 🔍 MONITOREO:
echo   comandos-desarrollo.bat logs             - Ver logs de todos los servicios
echo   comandos-desarrollo.bat logs-backend     - Ver logs solo del backend
echo   comandos-desarrollo.bat logs-db          - Ver logs solo de PostgreSQL
echo   comandos-desarrollo.bat ps               - Ver contenedores activos
echo   comandos-desarrollo.bat health           - Verificar salud de servicios
echo.
echo 🛠️ TROUBLESHOOTING:
echo   comandos-desarrollo.bat clean-docker     - Limpiar recursos Docker no utilizados
echo   comandos-desarrollo.bat reset            - Reset completo (PELIGROSO)
echo.
echo 🌐 ABRIR URLs:
echo   comandos-desarrollo.bat open api         - Abrir Backend API
echo   comandos-desarrollo.bat open docs        - Abrir API Docs
echo   comandos-desarrollo.bat open frontend    - Abrir Frontend
echo   comandos-desarrollo.bat open pgadmin     - Abrir PgAdmin
echo.
echo 🌐 URLs ÚTILES:
echo   Backend API:    http://localhost:8000
echo   API Docs:       http://localhost:8000/docs
echo   Frontend:       http://localhost:3000
echo   PgAdmin:        http://localhost:5050 (admin@monitoreo.dev / admin123)
echo.
goto end

:dev_start
echo 🚀 Iniciando entorno de desarrollo...
python devtools/orquestador_desarrollo.py iniciar
goto end

:dev_start_rebuild
echo 🚀 Iniciando con rebuild de imágenes Docker...
python devtools/orquestador_desarrollo.py iniciar --rebuild
goto end

:dev_start_pgadmin
echo 🚀 Iniciando entorno con PgAdmin...
docker-compose -f docker-compose.debug.yml --profile pgadmin up -d
goto end

:dev_status
echo 🔍 Verificando estado del entorno...
python devtools/orquestador_desarrollo.py diagnosticar
goto end

:dev_stop
echo ⬇️ Parando entorno (con backup automático)...
python devtools/orquestador_desarrollo.py terminar
goto end

:dev_stop_clean
echo 🧹 Parando y limpiando completamente...
echo ⚠️ ESTO ELIMINARÁ TODOS LOS DATOS DE DESARROLLO
set /p confirm="¿Estás seguro? (s/N): "
if /i "%confirm%"=="s" (
    python devtools/orquestador_desarrollo.py terminar --limpiar-completo
) else (
    echo Operación cancelada
)
goto end

:dev_restart
echo 🔄 Regenerando entorno completo...
python devtools/orquestador_desarrollo.py regenerar
goto end

:dev_backup
echo 💾 Creando backup manual...
python devtools/orquestador_desarrollo.py backup
goto end

:dev_logs
echo 📋 Mostrando logs de todos los servicios...
docker-compose -f docker-compose.debug.yml logs -f
goto end

:dev_logs_backend
echo 📋 Mostrando logs del backend...
docker logs -f backend_debug 2>nul || echo Backend no está ejecutándose
goto end

:dev_logs_db
echo 📋 Mostrando logs de PostgreSQL...
docker logs -f postgres_debug 2>nul || echo PostgreSQL no está ejecutándose
goto end

:dev_ps
echo 📦 Contenedores activos:
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
goto end

:dev_health
echo 🏥 Verificando salud de servicios...
echo.

REM Backend API
curl -s -f http://localhost:8000/health >nul 2>&1
if !errorlevel! equ 0 (
    echo   Backend API:    ✅ Healthy
) else (
    echo   Backend API:    ❌ No responde
)

REM Frontend
curl -s -f http://localhost:3000 >nul 2>&1
if !errorlevel! equ 0 (
    echo   Frontend:       ✅ Accessible
) else (
    echo   Frontend:       ❌ No responde
)

REM PostgreSQL
docker exec postgres_debug pg_isready -U vnm_user >nul 2>&1
if !errorlevel! equ 0 (
    echo   PostgreSQL:     ✅ Ready
) else (
    echo   PostgreSQL:     ❌ No disponible
)

REM Redis
docker exec redis_debug redis-cli ping >nul 2>&1
if !errorlevel! equ 0 (
    echo   Redis:          ✅ Responding
) else (
    echo   Redis:          ❌ No disponible
)
goto end

:dev_clean_docker
echo 🧹 Limpiando recursos Docker no utilizados...
docker system prune -f
docker volume prune -f
goto end

:dev_reset
echo 💥 RESET COMPLETO DEL ENTORNO
echo ⚠️ ESTO ELIMINARÁ TODO: contenedores, volúmenes, imágenes
set /p confirm="¿Estás COMPLETAMENTE seguro? (escriba 'RESET' para confirmar): "
if "%confirm%"=="RESET" (
    echo 🔥 Ejecutando reset completo...
    python devtools/orquestador_desarrollo.py terminar --limpiar-completo --sin-backup
    docker system prune -a -f
    docker volume prune -f
    echo ✅ Reset completo terminado
) else (
    echo Operación cancelada
)
goto end

:dev_open
if "%2"=="api" start http://localhost:8000
if "%2"=="backend" start http://localhost:8000
if "%2"=="docs" start http://localhost:8000/docs
if "%2"=="frontend" start http://localhost:3000
if "%2"=="web" start http://localhost:3000
if "%2"=="pgadmin" start http://localhost:5050
if "%2"=="admin" start http://localhost:5050
if "%2"=="" echo Uso: comandos-desarrollo.bat open {api^|docs^|frontend^|pgadmin}
goto end

:end
endlocal
