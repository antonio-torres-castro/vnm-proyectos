# Orquestador de Desarrollo VNM-Proyectos

## 🎯 Descripción

El **Orquestador de Desarrollo** es un programa unificado en Python que gestiona el ciclo de vida completo de los contenedores Docker del proyecto VNM de forma **idempotente** y **robusta**.

## 🚀 Características Principales

- ✅ **Idempotente**: Mismos resultados en cada ejecución
- 🔍 **Diagnóstico Completo**: Verificación de estado y conectividad
- 🛡️ **Backup Automático**: Respaldo automático antes de operaciones destructivas
- 📊 **Logging Detallado**: Registros completos de todas las operaciones
- 🎨 **Interfaz Colorida**: Output claro y fácil de entender
- ⚡ **Operaciones Robustas**: Manejo de errores y recuperación automática

## 📁 Estructura de Archivos

```
/workspace/
├── orquestador_desarrollo.py    # Orquestador principal (completo)
├── desarrollo.py                # Script de acceso rápido
├── docker-compose.yml           # Configuración producción
├── docker-compose.debug.yml     # Configuración debug/desarrollo
└── database/
    ├── backups/                 # Backups automáticos
    ├── init-data/              # Scripts de inicialización
    └── scripts/                # Scripts de utilidades
```

## 🎮 Comandos Rápidos (desarrollo.py)

### Comandos Básicos
```bash
# Diagnosticar estado actual
python desarrollo.py

# Iniciar entorno completo
python desarrollo.py up

# Terminar entorno (con backup automático)
python desarrollo.py down

# Reiniciar entorno
python desarrollo.py restart

# Limpieza completa + regenerar
python desarrollo.py clean
```

### Comandos de Logs
```bash
# Ver todos los logs
python desarrollo.py logs

# Ver logs específicos
python desarrollo.py logs backend
python desarrollo.py logs postgres
python desarrollo.py logs frontend
```

### Comandos Avanzados
```bash
# Diagnóstico detallado
python desarrollo.py diagnosticar

# Backup manual
python desarrollo.py backup

# Regenerar completamente
python desarrollo.py regenerar
```

## 🔧 Orquestador Completo (orquestador_desarrollo.py)

### Sintaxis General
```bash
python orquestador_desarrollo.py <accion> [opciones]
```

### Acciones Disponibles

#### 1. `diagnosticar`
Verifica el estado completo del entorno y genera un reporte detallado.

```bash
# Diagnóstico básico
python orquestador_desarrollo.py diagnosticar

# Diagnóstico detallado
python orquestador_desarrollo.py diagnosticar --verboso
```

**Salidas:**
- Estado de cada contenedor
- Verificación de conectividad
- Health checks
- Reporte JSON completo
- Código de salida: 0 (todo OK) o 1 (problemas)

#### 2. `iniciar`
Levanta el entorno completo con verificaciones de salud.

```bash
# Inicio normal
python orquestador_desarrollo.py iniciar

# Inicio con rebuild forzado
python orquestador_desarrollo.py iniciar --rebuild

# Modo producción
python orquestador_desarrollo.py iniciar --modo produccion
```

**Proceso:**
1. Verificación de estado actual
2. Parada de servicios conflictivos
3. Inicio de servicios
4. Verificación de salud (timeout 120s)
5. Reporte de URLs disponibles

#### 3. `terminar`
Para el entorno con opciones de backup y limpieza.

```bash
# Terminación normal (con backup)
python orquestador_desarrollo.py terminar

# Terminación sin backup
python orquestador_desarrollo.py terminar --sin-backup

# Limpieza completa (elimina volúmenes)
python orquestador_desarrollo.py terminar --limpiar-completo
```

**Proceso:**
1. Backup automático de PostgreSQL (opcional)
2. Parada de contenedores
3. Limpieza de recursos (opcional)
4. Verificación final

#### 4. `regenerar`
Recreación completa del entorno con configuración fresca.

```bash
# Regeneración completa
python orquestador_desarrollo.py regenerar
```

**Proceso:**
1. Backup de seguridad
2. Limpieza completa
3. Rebuild de imágenes
4. Inicio con verificaciones
5. Validación final

#### 5. `backup`
Crea backup manual de la base de datos.

```bash
# Backup manual
python orquestador_desarrollo.py backup
```

**Características del Backup:**
- Formato: `backup_YYYYMMDD_HHMMSS.sql.zip`
- Compresión automática
- Retención: últimos 10 backups
- Ubicación: `database/backups/`

### Opciones Globales

| Opción | Descripción | Default |
|--------|-------------|---------|
| `--modo` | `debug` o `produccion` | `debug` |
| `--verboso` | Información detallada | `false` |
| `--rebuild` | Forzar rebuild de imágenes | `false` |
| `--sin-backup` | No crear backup | `false` |
| `--limpiar-completo` | Eliminar volúmenes | `false` |

## 🏗️ Servicios Gestionados

### Modo Debug (docker-compose.debug.yml)
- **postgres**: `vnm_postgres_debug` - Puerto 5432
- **backend**: `vnm_backend_debug` - Puerto 8000 + 5678 (debug)
- **frontend**: `vnm_frontend_debug` - Puerto 3000

### Modo Producción (docker-compose.yml)
- **postgres**: `monitoreo_postgres` - Puerto 5432
- **pgadmin**: `monitoreo_pgadmin` - Puerto 8081
- **backend**: `monitoreo_backend` - Puerto 8000
- **frontend**: `monitoreo_frontend` - Puerto 3000

## 🔍 Verificaciones de Salud

### PostgreSQL
- Verificación con `pg_isready`
- Test de conectividad a la base
- Health check del contenedor

### Backend (FastAPI)
- Verificación HTTP en `/docs`
- Estado del contenedor
- Verificación de dependencias

### Frontend (React)
- Verificación HTTP en puerto 3000
- Estado del contenedor
- Verificación de hot reload

## 📊 Logging y Diagnósticos

### Archivos de Log
- `orquestador.log`: Log detallado de operaciones
- `diagnostico_TIMESTAMP.json`: Reportes de diagnóstico

### Estructura del Diagnóstico JSON
```json
{
  "timestamp": "2025-10-14T09:00:47",
  "modo": "debug",
  "docker_compose_file": "docker-compose.debug.yml",
  "servicios": {
    "postgres": {
      "contenedor": "vnm_postgres_debug",
      "estado": "healthy",
      "puerto": 5432,
      "conectividad": true,
      "detalles": {...}
    }
  },
  "resumen": {
    "servicios_saludables": 3,
    "servicios_ejecutando": 3,
    "total_servicios": 3,
    "entorno_operativo": true
  }
}
```

## 🛠️ Flujo de Trabajo Recomendado

### Desarrollo Diario
```bash
# 1. Iniciar día de desarrollo
python desarrollo.py up

# 2. Verificar estado si hay problemas
python desarrollo.py diagnosticar

# 3. Ver logs si necesario
python desarrollo.py logs backend

# 4. Al final del día
python desarrollo.py down
```

### Debugging en VS Code
```bash
# 1. Iniciar entorno en modo debug
python desarrollo.py up

# 2. Abrir VS Code
code .

# 3. Presionar F5 → "Backend: FastAPI Docker Debug"
# 4. El backend estará disponible en http://localhost:8000
```

### Problemas y Regeneración
```bash
# Si hay problemas irrecuperables
python desarrollo.py clean

# O regeneración manual completa
python orquestador_desarrollo.py regenerar --verboso
```

## ⚡ URLs de Servicios

Después de ejecutar `python desarrollo.py up`:

| Servicio | URL | Descripción |
|----------|-----|-------------|
| Frontend | http://localhost:3000 | Aplicación React |
| Backend API | http://localhost:8000 | API FastAPI |
| Backend Docs | http://localhost:8000/docs | Documentación Swagger |
| PostgreSQL | localhost:5432 | Base de datos |
| Debug Server | localhost:5678 | Puerto de debugging |

## 🎯 Características de Idempotencia

El orquestador garantiza **idempotencia** mediante:

1. **Verificación de Estado**: Siempre verifica el estado actual antes de actuar
2. **Operaciones Condicionales**: Solo ejecuta acciones necesarias
3. **Rollback Automático**: Revierte cambios en caso de errores
4. **Estado Consistente**: Garantiza que múltiples ejecuciones produzcan el mismo resultado
5. **Verificación Post-Acción**: Confirma que las operaciones se completaron correctamente

## 🚨 Códigos de Salida

| Código | Significado |
|--------|-------------|
| `0` | Operación exitosa |
| `1` | Error en la operación |
| `130` | Interrumpido por usuario (Ctrl+C) |

## 🔧 Solución de Problemas

### Error: "Docker no está ejecutándose"
```bash
# Verificar Docker
docker --version
docker-compose --version

# Iniciar Docker si está parado
sudo systemctl start docker
```

### Error: "Archivo docker-compose no encontrado"
```bash
# Verificar directorio actual
ls -la docker-compose*.yml

# Navegar al directorio correcto
cd /ruta/al/proyecto
```

### Error: "Servicios no responden"
```bash
# Diagnóstico detallado
python desarrollo.py diagnosticar

# Ver logs específicos
python desarrollo.py logs [servicio]

# Regenerar entorno
python desarrollo.py clean
```

### Error: "Puerto en uso"
```bash
# Verificar puertos en uso
netstat -tlnp | grep ':8000\|:3000\|:5432'

# Parar servicios conflictivos
python desarrollo.py down

# Regenerar con limpieza
python desarrollo.py clean
```

## 📝 Mantenimiento

### Limpieza de Backups
Los backups se mantienen automáticamente (últimos 10), pero se pueden limpiar manualmente:
```bash
ls -la database/backups/
rm database/backups/backup_20241001_*.sql.zip
```

### Limpieza de Logs
```bash
# Rotar logs del orquestador
mv orquestador.log orquestador.log.old

# Limpiar logs de Docker
docker system prune -f
```

### Actualización de Imágenes
```bash
# Forzar rebuild de todas las imágenes
python orquestador_desarrollo.py iniciar --rebuild

# O regeneración completa
python desarrollo.py clean
```

## 🤝 Integración con PowerShell (Migración)

Para migrar desde los scripts PowerShell existentes:

| Script PowerShell | Comando Equivalente |
|------------------|-------------------|
| `inicio-desarrollo.ps1` | `python desarrollo.py up` |
| `cerrar-desarrollo.ps1` | `python desarrollo.py down` |
| `cerrar-desarrollo.ps1 -LimpiarCompleto` | `python desarrollo.py clean` |

## 👤 Autor

**MiniMax Agent** - Orquestador de Desarrollo VNM-Proyectos

---

> 💡 **Tip**: Para obtener ayuda rápida en cualquier momento, ejecuta `python desarrollo.py help`
