#!/bin/bash
# inicio-desarrollo.sh
# Script para iniciar el entorno de desarrollo completo

echo -e "\033[36m🚀 INICIANDO ENTORNO DE DESARROLLO VNM-PROYECTOS\033[0m"
echo -e "\033[36m============================================================\033[0m"

# Verificar que estamos en el directorio correcto
if [ ! -f "docker-compose.debug.yml" ]; then
    echo -e "\033[31m❌ Error: docker-compose.debug.yml no encontrado\033[0m"
    echo -e "\033[33m📁 Asegúrate de estar en el directorio vnm-proyectos\033[0m"
    exit 1
fi

echo -e "\033[32m📁 Directorio: $(pwd)\033[0m"
echo ""

# Paso 1: Limpiar entorno previo si existe
echo -e "\033[33m🧹 Paso 1: Limpiando entorno previo...\033[0m"
docker-compose -f docker-compose.debug.yml down -v >/dev/null 2>&1
sleep 2

# Paso 2: Levantar servicios
echo -e "\033[33m🏗️  Paso 2: Iniciando servicios...\033[0m"
echo "   - PostgreSQL Database"
echo "   - Backend FastAPI (modo debug)"  
echo "   - Frontend React"
echo ""

docker-compose -f docker-compose.debug.yml up -d

# Paso 3: Esperar a que los servicios estén listos
echo -e "\033[33m⏳ Paso 3: Esperando a que los servicios estén listos...\033[0m"

timeout=60
elapsed=0
all_ready=false

while [ "$all_ready" = false ] && [ $elapsed -lt $timeout ]; do
    postgres_ready=$(docker exec vnm_postgres_debug pg_isready -U monitoreo_user -d monitoreo_dev 2>/dev/null | grep -q "accepting connections" && echo "true" || echo "false")
    backend_running=$(docker ps --filter "name=vnm_backend_debug" --filter "status=running" --quiet | wc -l)
    frontend_running=$(docker ps --filter "name=vnm_frontend_debug" --filter "status=running" --quiet | wc -l)
    
    if [ "$postgres_ready" = "true" ] && [ "$backend_running" -gt 0 ] && [ "$frontend_running" -gt 0 ]; then
        all_ready=true
    else
        echo "   Esperando servicios..."
        sleep 5
        elapsed=$((elapsed + 5))
    fi
done

if [ "$all_ready" = false ]; then
    echo -e "\033[31m⚠️  Timeout: Los servicios tardaron más de lo esperado\033[0m"
    echo -e "\033[33mVerifica manualmente con: docker ps\033[0m"
else
    echo -e "\033[32m✅ Todos los servicios están listos!\033[0m"
fi

echo ""

# Paso 4: Mostrar estado
echo -e "\033[33m📊 Paso 4: Estado de los servicios:\033[0m"
echo ""

docker ps --filter "name=vnm_" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

echo ""

# Paso 5: Verificar conectividad
echo -e "\033[33m🔍 Paso 5: Verificando conectividad...\033[0m"

# Test PostgreSQL
if docker exec vnm_postgres_debug pg_isready -U monitoreo_user -d monitoreo_dev >/dev/null 2>&1; then
    echo -e "   \033[32m✅ PostgreSQL: Conectado y listo\033[0m"
else
    echo -e "   \033[31m❌ PostgreSQL: No responde\033[0m"
fi

# Test Frontend
if curl -s --connect-timeout 5 http://localhost:3000 >/dev/null 2>&1; then
    echo -e "   \033[32m✅ Frontend React: Disponible en http://localhost:3000\033[0m"
else
    echo -e "   \033[33m⏳ Frontend React: Iniciando... (prueba http://localhost:3000 en 30s)\033[0m"
fi

# Test Backend (solo en modo normal, en debug esperará VS Code)
echo -e "   \033[33m⏳ Backend API: En modo debug - esperando VS Code\033[0m"
echo -e "     \033[36m💡 Para activar: F5 en VS Code → 'Backend: FastAPI Docker Debug'\033[0m"

echo ""

# Resumen final
echo -e "\033[32m🎉 ENTORNO LISTO PARA DESARROLLO\033[0m"
echo -e "\033[32m========================================\033[0m"
echo ""
echo -e "\033[36m📋 PRÓXIMOS PASOS:\033[0m"
echo -e "   1. Abrir VS Code en este directorio: code ."
echo -e "   2. Presionar F5 para iniciar debugging"  
echo -e "   3. Seleccionar: '🐍 Backend: FastAPI Docker Debug'"
echo -e "   4. ¡La API se activará en http://localhost:8000!"
echo ""
echo -e "\033[36m🌐 SERVICIOS DISPONIBLES:\033[0m"
echo -e "   • Frontend:     http://localhost:3000"
echo -e "   • Backend API:  http://localhost:8000 (después de F5)"
echo -e "   • PostgreSQL:   localhost:5432"
echo -e "   • Debug Server: localhost:5678"
echo ""
echo -e "\033[36m🔧 COMANDOS ÚTILES:\033[0m"
echo -e "   • Ver logs backend:  docker logs vnm_backend_debug -f"
echo -e "   • Ver logs postgres: docker logs vnm_postgres_debug -f"
echo -e "   • Parar todo:        docker-compose -f docker-compose.debug.yml down"
echo -e "   • Verificar estado:  ./verificar-database.sh"
echo ""
echo -e "\033[32m¡Feliz desarrollo! 🚀\033[0m"
