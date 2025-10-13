#!/bin/bash
# Script de verificación de conexión a base de datos

echo "🔍 Verificando conexión a base de datos..."

# Verificar que los contenedores estén ejecutándose
echo ""
echo "📦 Estado de contenedores:"
docker-compose -f docker-compose.debug.yml ps

# Verificar logs de postgres
echo ""
echo "🗄️  Últimos logs de PostgreSQL:"
docker logs vnm_postgres_debug --tail 10

# Verificar conectividad de postgres
echo ""
echo "🔗 Verificando conectividad de PostgreSQL..."
if docker exec vnm_postgres_debug pg_isready -U monitoreo_user -d monitoreo_dev > /dev/null 2>&1; then
    echo "✅ PostgreSQL está listo y acepta conexiones"
else
    echo "❌ PostgreSQL no está respondiendo"
    echo "💡 Intenta: docker-compose -f docker-compose.debug.yml restart postgres"
fi

# Verificar logs de backend
echo ""
echo "🐍 Últimos logs del Backend:"
docker logs vnm_backend_debug --tail 15

# Verificar si el backend está respondiendo
echo ""
echo "🌐 Verificando API del Backend..."
if curl -s -f "http://localhost:8000/api/v1/health" > /dev/null 2>&1; then
    echo "✅ API del backend está respondiendo"
    echo "📄 Respuesta:"
    curl -s "http://localhost:8000/api/v1/health" | python3 -m json.tool 2>/dev/null || echo "Respuesta no es JSON válido"
else
    echo "❌ API del backend no está respondiendo"
    echo "💡 Verifica los logs del backend arriba"
fi

# Verificar datos en base de datos
echo ""
echo "📊 Verificando datos en base de datos..."

USER_COUNT=$(docker exec vnm_postgres_debug psql -U monitoreo_user -d monitoreo_dev -t -c "SELECT COUNT(*) FROM seguridad.usuario;" 2>/dev/null | tr -d ' ')
if [ ! -z "$USER_COUNT" ] && [ "$USER_COUNT" != "" ]; then
    echo "✅ Tabla de usuarios encontrada. Usuarios: $USER_COUNT"
else
    echo "⚠️  No se pudo verificar tabla de usuarios"
fi

TABLE_COUNT=$(docker exec vnm_postgres_debug psql -U monitoreo_user -d monitoreo_dev -t -c "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema='seguridad';" 2>/dev/null | tr -d ' ')
if [ ! -z "$TABLE_COUNT" ] && [ "$TABLE_COUNT" != "" ]; then
    echo "✅ Esquema 'seguridad' encontrado. Tablas: $TABLE_COUNT"
else
    echo "⚠️  Esquema 'seguridad' no encontrado o inaccesible"
fi

echo ""
echo "🔧 Comandos útiles para debugging:"
echo "• Reiniciar postgres: docker-compose -f docker-compose.debug.yml restart postgres"
echo "• Ver logs postgres: docker logs vnm_postgres_debug -f"
echo "• Ver logs backend: docker logs vnm_backend_debug -f"
echo "• Conectar a DB: docker exec -it vnm_postgres_debug psql -U monitoreo_user -d monitoreo_dev"
echo "• Limpiar todo: docker-compose -f docker-compose.debug.yml down -v"

echo ""
echo "✅ Verificación completada!"
