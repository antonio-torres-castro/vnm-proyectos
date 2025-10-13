#!/bin/bash
# fix-bcrypt-error.sh
# Script para solucionar el error de bcrypt en el backend

echo -e "\033[36mSOLUCIONANDO ERROR DE BCRYPT\033[0m"
echo -e "\033[36m=================================================\033[0m"

# Verificar que estamos en el directorio correcto
if [ ! -f "docker-compose.debug.yml" ]; then
    echo -e "\033[31mError: docker-compose.debug.yml no encontrado\033[0m"
    echo -e "\033[33mAsegurate de estar en el directorio vnm-proyectos\033[0m"
    exit 1
fi

echo -e "\033[32mDirectorio: $(pwd)\033[0m"
echo ""

# Paso 1: Parar contenedores actuales
echo -e "\033[33mPaso 1: Parando contenedores actuales...\033[0m"
docker-compose -f docker-compose.debug.yml down

# Paso 2: Limpiar imagenes existentes del backend
echo -e "\033[33mPaso 2: Limpiando imagen del backend...\033[0m"
backend_image=$(docker images --filter "reference=vnm-proyectos-backend" --quiet)
if [ -n "$backend_image" ]; then
    echo -e "\033[33mRemoviendo imagen existente del backend...\033[0m"
    docker rmi $backend_image -f
else
    echo -e "\033[37mNo se encontro imagen existente del backend\033[0m"
fi

# Paso 3: Reconstruir imagen del backend con dependencias corregidas
echo -e "\033[33mPaso 3: Reconstruyendo imagen del backend...\033[0m"
echo -e "\033[36mEsto incluye:\033[0m"
echo "  - Herramientas de compilacion para bcrypt"
echo "  - Dependencias actualizadas"
echo "  - Bcrypt version estable"
echo ""

docker-compose -f docker-compose.debug.yml build --no-cache backend

# Verificar si la construccion fue exitosa
if [ $? -ne 0 ]; then
    echo -e "\033[31mError: Fallo la construccion del backend\033[0m"
    echo -e "\033[33mVerifica los logs arriba para mas detalles\033[0m"
    exit 1
fi

# Paso 4: Iniciar contenedores con imagen corregida
echo -e "\033[33mPaso 4: Iniciando contenedores con imagen corregida...\033[0m"
docker-compose -f docker-compose.debug.yml up -d

# Paso 5: Esperar y verificar que el backend inicie correctamente
echo -e "\033[33mPaso 5: Verificando que el backend inicie sin errores...\033[0m"

sleep 10

# Verificar logs del backend para errores de bcrypt
echo -e "\033[36mVerificando logs del backend...\033[0m"
backend_logs=$(docker logs vnm_backend_debug 2>&1)
if echo "$backend_logs" | grep -q "bcrypt.*error\|Traceback.*bcrypt"; then
    echo -e "\033[31mADVERTENCIA: Aun se detectan errores de bcrypt en los logs\033[0m"
    echo -e "\033[33mLogs del backend:\033[0m"
    docker logs vnm_backend_debug --tail 20
else
    echo -e "\033[32mBackend iniciando correctamente sin errores de bcrypt\033[0m"
fi

# Paso 6: Verificar estado final
echo -e "\033[33mPaso 6: Estado final de contenedores:\033[0m"
docker ps --filter "name=vnm_" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

echo ""
echo -e "\033[32mSOLUCION DE BCRYPT COMPLETADA\033[0m"
echo -e "\033[32m========================================\033[0m"
echo ""

echo -e "\033[36mPROXIMOS PASOS:\033[0m"
echo "1. Verificar que no hay errores: ./verificar-database.sh"
echo "2. Abrir VS Code: code ."
echo "3. Iniciar debugging: F5 -> Backend: FastAPI Docker Debug"
echo ""

echo -e "\033[33mSi el problema persiste:\033[0m"
echo "  - Ejecuta: docker logs vnm_backend_debug -f"
echo "  - Revisa los logs para errores especificos"
echo ""

echo -e "\033[32mSolucion aplicada!\033[0m"
