# 🚀 Flujo de Desarrollo Completo - VNM Proyectos

## 📋 Resumen de Comandos Principales

| Acción | Comando | Descripción |
|--------|---------|-------------|
| **Iniciar Desarrollo** | `python devtools/orquestador_desarrollo.py iniciar` | Levanta entorno completo |
| **Diagnosticar** | `python devtools/orquestador_desarrollo.py diagnosticar` | Verifica estado de servicios |
| **Parar (con backup)** | `python devtools/orquestador_desarrollo.py terminar` | Para servicios + backup automático |
| **Parar (limpio)** | `python devtools/orquestador_desarrollo.py terminar --limpiar-completo` | Para + elimina volúmenes |
| **Regenerar completo** | `python devtools/orquestador_desarrollo.py regenerar` | Recrear entorno desde cero |
| **Backup manual** | `python devtools/orquestador_desarrollo.py backup` | Backup de BD sin parar servicios |

---

## 🔄 1. LEVANTAR AMBIENTE DE DESARROLLO

### Opción A: Inicio Normal
```bash
# Inicio básico del entorno
python devtools/orquestador_desarrollo.py iniciar

# Con información detallada
python devtools/orquestador_desarrollo.py iniciar --verboso
```

### Opción B: Inicio con Rebuild (para cambios en Docker)
```bash
# Fuerza la reconstrucción de imágenes Docker
python devtools/orquestador_desarrollo.py iniciar --rebuild
```

### Opción C: Inicio con PgAdmin (opcional)
```bash
# Inicia entorno incluyendo PgAdmin para administrar BD
docker-compose -f docker-compose.debug.yml --profile pgadmin up -d
```

### Opción D: Depuración con VS Code
```bash
# En VS Code:
# 1. Presiona F5
# 2. Selecciona "FullStack Debug"
# 3. VS Code ejecuta automáticamente el orquestador + depuración
```

### ✅ Verificación de Inicio Exitoso
Después del inicio, deberías ver:
- ✅ `Entorno iniciado correctamente`
- ✅ URLs de servicios disponibles:
  - Backend API: `http://localhost:8000`
  - Frontend: `http://localhost:3000`
  - PgAdmin (si está activo): `http://localhost:5050`

---

## 🔍 2. DIAGNOSTICAR AMBIENTE

### Diagnóstico Básico
```bash
# Verifica estado general del entorno
python devtools/orquestador_desarrollo.py diagnosticar
```

### Diagnóstico Detallado
```bash
# Con información extendida
python devtools/orquestador_desarrollo.py diagnosticar --verboso
```

### 📊 Interpretación del Diagnóstico

#### ✅ Estado Saludable
```
✓ PostgreSQL: running (puerto 5432)
✓ Redis: running (puerto 6379)
✓ Backend API: healthy (puerto 8000)
✓ Frontend: running (puerto 3000)
🎉 ENTORNO COMPLETAMENTE OPERATIVO
```

#### ⚠️ Estado Problemático
```
✗ PostgreSQL: stopped
✓ Redis: running
⚠ Backend API: no response
✗ Frontend: not running
❌ ENTORNO PARCIALMENTE OPERATIVO
```

### 🛠️ Comandos de Diagnóstico Manual
```bash
# Verificar contenedores Docker
docker ps

# Ver logs de servicios específicos
docker logs postgres_debug
docker logs redis_debug
docker logs backend_debug

# Verificar conectividad de servicios
curl -s http://localhost:8000/health | jq
curl -s http://localhost:3000
```

---

## ⬇️ 3. PARAR AMBIENTE (CON BACKUP)

### Opción A: Parada Normal con Backup Automático
```bash
# Para servicios y crea backup de la BD automáticamente
python devtools/orquestador_desarrollo.py terminar
```

**¿Qué hace?**
- ✅ Para todos los contenedores Docker
- ✅ Crea backup automático de PostgreSQL
- ✅ Preserva volúmenes de datos
- ✅ Guarda backup en `.backups/` con timestamp

### Opción B: Parada Sin Backup
```bash
# Para servicios sin crear backup (más rápido)
python devtools/orquestador_desarrollo.py terminar --sin-backup
```

### Opción C: Parada con PgAdmin Incluido
```bash
# Si iniciaste con PgAdmin, inclúyelo en la parada
docker-compose -f docker-compose.debug.yml --profile pgadmin down
```

---

## 🧹 4. PARAR AMBIENTE (LIMPIEZA COMPLETA)

### Limpieza Completa
```bash
# Para servicios + elimina volúmenes + limpia datos
python devtools/orquestador_desarrollo.py terminar --limpiar-completo
```

**⚠️ ADVERTENCIA**: Esto elimina TODOS los datos de desarrollo.

**¿Qué hace?**
- ✅ Para todos los contenedores
- ✅ Crea backup antes de eliminar (a menos que uses --sin-backup)
- ❌ Elimina volúmenes de Docker
- ❌ Elimina datos de PostgreSQL
- ❌ Elimina datos de Redis
- ❌ Limpia cache de Docker

### Limpieza Completa Sin Backup (PELIGROSO)
```bash
# Elimina TODO sin backup - SOLO para resetear ambiente corrupto
python devtools/orquestador_desarrollo.py terminar --limpiar-completo --sin-backup
```

---

## 🔄 5. REGENERAR AMBIENTE COMPLETO

### Regeneración Automática
```bash
# Para + limpia + reconstruye + inicia
python devtools/orquestador_desarrollo.py regenerar
```

**¿Cuándo usar?**
- 🐛 Cuando el ambiente tiene problemas irrecuperables
- 🔄 Después de cambios importantes en Docker
- 🧹 Para empezar completamente limpio
- 📦 Después de actualizar dependencias

**¿Qué hace?**
1. Para servicios actuales
2. Crea backup de BD (si existe)
3. Elimina volúmenes y contenedores
4. Reconstruye imágenes Docker
5. Inicia ambiente limpio

---

## 💾 6. BACKUPS MANUALES

### Crear Backup Sin Parar Servicios
```bash
# Backup de BD mientras el entorno está ejecutándose
python devtools/orquestador_desarrollo.py backup
```

### Ubicación de Backups
```bash
# Los backups se guardan en:
.backups/
├── backup_vnm_db_2025-10-14_192159.sql   # Backup de BD
├── backup_vnm_db_2025-10-14_142301.sql
└── ...
```

### Restaurar Backup Manual
```bash
# Para restaurar un backup específico:
# 1. Para el entorno
python devtools/orquestador_desarrollo.py terminar

# 2. Restaura desde backup
docker-compose -f docker-compose.debug.yml up -d postgres
docker exec -i postgres_debug psql -U vnm_user -d vnm_db < .backups/backup_vnm_db_YYYY-MM-DD_HHMMSS.sql

# 3. Reinicia el entorno
python devtools/orquestador_desarrollo.py iniciar
```

---

## 🎯 7. FLUJOS DE TRABAJO COMUNES

### 📅 Inicio de Día de Desarrollo
```bash
# 1. Verificar estado
python devtools/orquestador_desarrollo.py diagnosticar

# 2a. Si está todo bien: continuar
# 2b. Si hay problemas: reiniciar
python devtools/orquestador_desarrollo.py iniciar

# 3. Abrir VS Code y depurar (opcional)
# Presiona F5 > "FullStack Debug"
```

### 🔄 Cambios en Docker/Dependencias
```bash
# Cuando cambias Dockerfile, requirements.txt, package.json:
python devtools/orquestador_desarrollo.py iniciar --rebuild
```

### 🛠️ Solucionar Problemas
```bash
# 1. Diagnóstico detallado
python devtools/orquestador_desarrollo.py diagnosticar --verboso

# 2. Si no se resuelve: regenerar
python devtools/orquestador_desarrollo.py regenerar
```

### 🏁 Fin de Día de Desarrollo
```bash
# Opción A: Parar con backup (recomendado)
python devtools/orquestador_desarrollo.py terminar

# Opción B: Dejar corriendo (para continuar mañana)
# No hacer nada - los contenedores siguen ejecutándose
```

### 🧹 Limpieza de Fin de Sprint/Proyecto
```bash
# Limpieza completa para liberar espacio
python devtools/orquestador_desarrollo.py terminar --limpiar-completo
```

---

## 🚀 8. DEPURACIÓN CON VS CODE

### Configuraciones Disponibles
1. **Frontend Debug**: Solo React
2. **Backend Debug**: Solo FastAPI
3. **FullStack Debug**: Ambos simultáneamente ⭐

### Flujo de Depuración
```bash
# 1. VS Code: Presiona F5
# 2. Selecciona "FullStack Debug"
# 3. VS Code ejecuta automáticamente:
#    - python devtools/orquestador_desarrollo.py iniciar
#    - Inicia backend FastAPI con depuración
#    - Inicia frontend React con depuración
#    - Abre Chrome con localhost:3000
```

### Colocar Breakpoints
- **Backend**: Coloca breakpoints en archivos `.py`
- **Frontend**: Coloca breakpoints en archivos `.ts/.tsx`
- **Ambos** se pausarán cuando se ejecute el código

---

## 🐛 9. TROUBLESHOOTING COMÚN

### Error: "Docker no está ejecutándose"
```bash
# Linux/macOS:
sudo systemctl start docker

# Windows:
# Inicia Docker Desktop
```

### Error: "Puerto ya en uso"
```bash
# Verifica qué está usando el puerto
sudo netstat -tlnp | grep :8000

# Para los contenedores existentes
docker-compose -f docker-compose.debug.yml down
```

### Error: "Base de datos corrupta"
```bash
# Regenera el entorno completo
python devtools/orquestador_desarrollo.py regenerar
```

### Error: "Volúmenes llenos"
```bash
# Limpia volúmenes no utilizados
docker volume prune

# O limpieza completa del proyecto
python devtools/orquestador_desarrollo.py terminar --limpiar-completo
```

### Error: "Frontend no carga"
```bash
# Verifica logs del frontend
docker logs frontend_debug

# Reinstala dependencias
cd frontend && npm install
```

---

## 📊 10. MONITOREO CONTINUO

### Comandos Útiles Durante Desarrollo
```bash
# Ver logs en tiempo real
docker-compose -f docker-compose.debug.yml logs -f

# Ver logs de un servicio específico
docker logs -f postgres_debug
docker logs -f backend_debug

# Verificar uso de recursos
docker stats

# Ver estado de volúmenes
docker volume ls
```

### URLs de Monitoreo
- **API Health**: http://localhost:8000/health
- **API Docs**: http://localhost:8000/docs
- **Frontend**: http://localhost:3000
- **PgAdmin** (si activo): http://localhost:5050
  - Usuario: `admin@monitoreo.dev`
  - Contraseña: `admin123`

---

## 🎯 RESUMEN EJECUTIVO

### ✅ Para Desarrollo Diario:
1. **Iniciar**: `python devtools/orquestador_desarrollo.py iniciar`
2. **Verificar**: `python devtools/orquestador_desarrollo.py diagnosticar`
3. **Desarrollar**: Usar VS Code con F5 > "FullStack Debug"
4. **Terminar**: `python devtools/orquestador_desarrollo.py terminar`

### 🔄 Para Cambios Importantes:
1. **Rebuild**: `python devtools/orquestador_desarrollo.py iniciar --rebuild`
2. **Regenerar**: `python devtools/orquestador_desarrollo.py regenerar`

### 🧹 Para Limpieza:
1. **Con backup**: `python devtools/orquestador_desarrollo.py terminar`
2. **Limpio**: `python devtools/orquestador_desarrollo.py terminar --limpiar-completo`

---

**Autor**: MiniMax Agent  
**Fecha**: 2025-10-14  
**Versión**: 1.0 - Flujo Completo de Desarrollo
