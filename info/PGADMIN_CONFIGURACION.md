# Configuración de PgAdmin en Modo Debug

## Resumen

PgAdmin ha sido agregado como un **servicio opcional** en el entorno de desarrollo (modo debug) para permitir la administración gráfica de la base de datos PostgreSQL sin afectar el rendimiento del entorno básico de desarrollo.

## ¿Por qué es opcional?

En el entorno de desarrollo/debug, PgAdmin se mantiene como opcional para:

1. **Rendimiento**: Reducir el uso de recursos cuando no se necesita administración de BD
2. **Tiempo de inicio**: Acelerar el tiempo de arranque del entorno básico
3. **Flexibilidad**: Permitir a los desarrolladores decidir cuándo necesitan la interfaz gráfica

## Cómo activar PgAdmin

### Opción 1: Iniciar todo el entorno con PgAdmin
```bash
# Iniciar con el perfil pgadmin activado
docker-compose --profile pgadmin up -d

# O usando el orquestador (cuando esté disponible)
python devtools/orquestador_desarrollo.py iniciar --modo debug --profile pgadmin
```

### Opción 2: Agregar PgAdmin a un entorno ya ejecutándose
```bash
# Si ya tienes postgres/backend/frontend ejecutándose
docker-compose --profile pgadmin up pgadmin -d
```

### Opción 3: Solo PgAdmin y PostgreSQL
```bash
# Solo la base de datos y PgAdmin para administración
docker-compose up postgres pgadmin -d
```

## Acceso a PgAdmin

- **URL**: http://localhost:5050
- **Email**: admin@monitoreo.dev
- **Contraseña**: admin123

## Configuración preestablecida

PgAdmin viene configurado automáticamente con:

- **Servidor preconfigurado**: "Monitoreo PostgreSQL (Debug)"
- **Host**: postgres (nombre del contenedor)
- **Puerto**: 5432
- **Base de datos**: monitoreo_dev
- **Usuario**: monitoreo_user

## Verificación del estado

El orquestador de desarrollo detecta automáticamente si PgAdmin está ejecutándose:

```bash
python devtools/orquestador_desarrollo.py diagnosticar --modo debug
```

El diagnóstico mostrará:
- ✅ Servicios principales (postgres, backend, frontend)
- 📦 Servicios opcionales ejecutándose (incluyendo pgadmin si está activo)
- ℹ️ Instrucciones para activar servicios opcionales

## Archivos modificados

1. **docker-compose.debug.yml**: Agregado servicio pgadmin con perfil opcional
2. **devtools/pgadmin/servers.json**: Configuración preestablecida del servidor
3. **devtools/orquestador_desarrollo.py**: Soporte para servicios opcionales

## Beneficios

- **Desarrollo ágil**: Inicio rápido sin PgAdmin
- **Administración completa**: Interfaz gráfica cuando se necesite
- **Configuración automática**: Sin necesidad de configurar conexiones manualmente
- **Integración transparente**: Funciona con el sistema de diagnóstico existente

Autor: MiniMax Agent
