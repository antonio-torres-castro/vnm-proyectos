# Ejemplo de Salida del Orquestador

## 🔍 Comando: `python desarrollo.py`

```
🔧 DIAGNÓSTICO DEL ENTORNO DE DESARROLLO
============================================================
► Verificando servicio: postgres
  ✓ postgres: SALUDABLE
► Verificando servicio: backend
  ✓ backend: EJECUTANDO
► Verificando servicio: frontend
  ✓ frontend: EJECUTANDO

► RESUMEN DEL DIAGNÓSTICO
✓ Entorno completamente operativo

ℹ Diagnóstico guardado en: diagnostico_20241014_090047.json
```

## 🚀 Comando: `python desarrollo.py up`

```
🔧 INICIANDO ENTORNO DE DESARROLLO
============================================================
► Paso 1: Verificando estado actual
🔧 DIAGNÓSTICO DEL ENTORNO DE DESARROLLO
============================================================
► Verificando servicio: postgres
  ✗ postgres: NO EXISTE
► Verificando servicio: backend
  ✗ backend: NO EXISTE
► Verificando servicio: frontend
  ✗ frontend: NO EXISTE

► RESUMEN DEL DIAGNÓSTICO
⚠ Servicios operativos: 0/3

ℹ Diagnóstico guardado en: diagnostico_20241014_090000.json

► Paso 3: Iniciando servicios
ℹ Forzando rebuild de imágenes Docker

► Paso 4: Verificando servicios (timeout: 120s)
🔧 DIAGNÓSTICO DEL ENTORNO DE DESARROLLO
============================================================
► Verificando servicio: postgres
  ✓ postgres: SALUDABLE
► Verificando servicio: backend
  ✓ backend: EJECUTANDO
► Verificando servicio: frontend
  ✓ frontend: EJECUTANDO

► RESUMEN DEL DIAGNÓSTICO
✓ Entorno completamente operativo

ℹ Diagnóstico guardado en: diagnostico_20241014_090125.json
✓ Todos los servicios están operativos

► Paso 5: Resumen final
🔧 DIAGNÓSTICO DEL ENTORNO DE DESARROLLO
============================================================
► Verificando servicio: postgres
  ✓ postgres: SALUDABLE
► Verificando servicio: backend
  ✓ backend: EJECUTANDO
► Verificando servicio: frontend
  ✓ frontend: EJECUTANDO

► RESUMEN DEL DIAGNÓSTICO
✓ Entorno completamente operativo

ℹ Diagnóstico guardado en: diagnostico_20241014_090130.json
✓ ENTORNO LISTO PARA DESARROLLO

► SERVICIOS DISPONIBLES
  • Frontend: http://localhost:3000
  • Backend API: http://localhost:8000
  • Backend Docs: http://localhost:8000/docs
  • PostgreSQL: localhost:5432
  • Debug Server: localhost:5678
```

## 🛑 Comando: `python desarrollo.py down`

```
🔧 TERMINANDO ENTORNO DE DESARROLLO
============================================================
► Creando backup de la base de datos
ℹ Ejecutando pg_dumpall...
✓ Backup creado: backup_20241014_090200.sql.zip (2.45 MB)

► Parando contenedores
✓ Entorno cerrado (datos preservados)

► Verificando estado final
🔧 DIAGNÓSTICO DEL ENTORNO DE DESARROLLO
============================================================
► Verificando servicio: postgres
  ✗ postgres: DETENIDO
► Verificando servicio: backend
  ✗ backend: DETENIDO
► Verificando servicio: frontend
  ✗ frontend: DETENIDO

► RESUMEN DEL DIAGNÓSTICO
⚠ Servicios operativos: 0/3

ℹ Diagnóstico guardado en: diagnostico_20241014_090205.json
✓ Todos los contenedores han sido detenidos
```

## 🔄 Comando: `python desarrollo.py restart`

```
🔄 Reiniciando entorno...

🔧 TERMINANDO ENTORNO DE DESARROLLO
============================================================
► Creando backup de la base de datos
ℹ Ejecutando pg_dumpall...
✓ Backup creado: backup_20241014_090300.sql.zip (2.45 MB)

► Parando contenedores
✓ Entorno cerrado (datos preservados)

► Verificando estado final
✓ Todos los contenedores han sido detenidos

🔧 INICIANDO ENTORNO DE DESARROLLO
============================================================
► Paso 1: Verificando estado actual
► Paso 3: Iniciando servicios
► Paso 4: Verificando servicios (timeout: 120s)
✓ Todos los servicios están operativos
► Paso 5: Resumen final
✓ ENTORNO LISTO PARA DESARROLLO

► SERVICIOS DISPONIBLES
  • Frontend: http://localhost:3000
  • Backend API: http://localhost:8000
  • Backend Docs: http://localhost:8000/docs
  • PostgreSQL: localhost:5432
  • Debug Server: localhost:5678
```

## 🧹 Comando: `python desarrollo.py clean`

```
🔧 REGENERANDO ENTORNO COMPLETO
============================================================
► Paso 1: Creando backup de seguridad
► Creando backup de la base de datos
ℹ Ejecutando pg_dumpall...
✓ Backup creado: backup_20241014_090400.sql.zip (2.45 MB)

► Paso 2: Limpieza completa del entorno
🔧 LIMPIEZA COMPLETA
============================================================
► Parando contenedores
► Limpiando imágenes Docker no utilizadas
✓ Limpieza completa finalizada
⚠ Todos los datos de la base de datos han sido eliminados

► Paso 3: Reconstruyendo entorno
🔧 INICIANDO ENTORNO DE DESARROLLO
============================================================
► Paso 1: Verificando estado actual
► Paso 3: Iniciando servicios
ℹ Forzando rebuild de imágenes Docker
► Paso 4: Verificando servicios (timeout: 120s)
✓ Todos los servicios están operativos
► Paso 5: Resumen final
✓ ENTORNO LISTO PARA DESARROLLO

✓ REGENERACIÓN COMPLETADA EXITOSAMENTE
ℹ Backup de seguridad disponible en: /workspace/database/backups/backup_20241014_090400.sql.zip
```

## 📊 Comando: `python desarrollo.py logs backend`

```
vnm_backend_debug  | INFO:     Will watch for changes in these directories: ['/app']
vnm_backend_debug  | INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
vnm_backend_debug  | INFO:     Started reloader process [1] using StatReload
vnm_backend_debug  | INFO:     Started server process [8]
vnm_backend_debug  | INFO:     Waiting for application startup.
vnm_backend_debug  | INFO:     Application startup complete.
vnm_backend_debug  | INFO:     192.168.1.1:52342 - "GET /docs HTTP/1.1" 200 OK
vnm_backend_debug  | INFO:     192.168.1.1:52342 - "GET /openapi.json HTTP/1.1" 200 OK
```

## 💾 Comando: `python desarrollo.py backup`

```
► Creando backup de la base de datos
ℹ Ejecutando pg_dumpall...
✓ Backup creado: backup_20241014_090500.sql.zip (2.45 MB)
ℹ Eliminado backup antiguo: backup_20241001_120000.sql.zip

Resumen de backups:
Name                             LastWriteTime           Size(MB)
----                             -------------           --------
backup_20241014_090500.sql.zip  2024-10-14 09:05:00     2.45
backup_20241014_090400.sql.zip  2024-10-14 09:04:00     2.45
backup_20241014_090300.sql.zip  2024-10-14 09:03:00     2.45
```

## ❌ Ejemplo de Error y Recuperación

```
🔧 INICIANDO ENTORNO DE DESARROLLO
============================================================
► Paso 1: Verificando estado actual
► Paso 3: Iniciando servicios
► Paso 4: Verificando servicios (timeout: 120s)
ℹ Esperando servicios...
ℹ Esperando servicios...
⚠ Timeout alcanzado. Algunos servicios pueden no estar listos.
✗ Servicio problemático: backend
ℹ Revisar logs: docker logs vnm_backend_debug

► Paso 5: Resumen final
✗ Algunos servicios no están completamente operativos

# Para solucionar:
python desarrollo.py logs backend  # Ver qué está fallando
python desarrollo.py clean         # Regenerar completamente
```

## 📈 Archivo de Diagnóstico JSON

```json
{
  "timestamp": "2024-10-14T09:00:47.123456",
  "modo": "debug",
  "docker_compose_file": "docker-compose.debug.yml",
  "servicios": {
    "postgres": {
      "contenedor": "vnm_postgres_debug",
      "estado": "healthy",
      "puerto": 5432,
      "healthcheck_disponible": true,
      "dependencias": [],
      "conectividad": true,
      "detalles": {
        "ID": "abc123",
        "Names": "vnm_postgres_debug",
        "State": "running",
        "Status": "Up 2 minutes (healthy)"
      }
    },
    "backend": {
      "contenedor": "vnm_backend_debug",
      "estado": "running",
      "puerto": 8000,
      "healthcheck_disponible": false,
      "dependencias": ["postgres"],
      "conectividad": true,
      "detalles": {
        "ID": "def456",
        "Names": "vnm_backend_debug",
        "State": "running",
        "Status": "Up 1 minute"
      }
    },
    "frontend": {
      "contenedor": "vnm_frontend_debug",
      "estado": "running",
      "puerto": 3000,
      "healthcheck_disponible": false,
      "dependencias": ["backend"],
      "conectividad": true,
      "detalles": {
        "ID": "ghi789",
        "Names": "vnm_frontend_debug",
        "State": "running",
        "Status": "Up 30 seconds"
      }
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

## 💡 Código de Salida

Todos los comandos retornan:
- **0**: Operación exitosa
- **1**: Error en la operación  
- **130**: Interrumpido por usuario (Ctrl+C)

```bash
# Verificar código de salida
python desarrollo.py up
echo "Código de salida: $?"

# En scripts bash
if python desarrollo.py up; then
    echo "Entorno iniciado correctamente"
else
    echo "Error iniciando entorno"
    exit 1
fi
```
