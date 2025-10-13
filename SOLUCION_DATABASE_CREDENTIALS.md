# 🔧 Solución: Error de Credenciales de Base de Datos

## ❌ **Error encontrado:**
```
sqlalchemy.exc.OperationalError: (psycopg2.OperationalError) connection to server at "postgres" (172.19.0.2), port 5432 failed: FATAL: password authentication failed for user "monitoreo_user"
```

## 🔍 **Causa del problema:**
**Inconsistencia de credenciales** entre `docker-compose.debug.yml` y la configuración del backend.

### **Backend esperaba:**
```python
DATABASE_URL = "postgresql://monitoreo_user:monitoreo_pass@postgres:5432/monitoreo_dev"
```

### **Pero docker-compose.debug.yml tenía:**
```yaml
POSTGRES_USER: postgres           # ❌ Incorrecto
POSTGRES_PASSWORD: postgres123    # ❌ Incorrecto  
POSTGRES_DB: monitoreo_db         # ❌ Incorrecto
```

## ✅ **Corrección aplicada:**

### **1. Actualizado docker-compose.debug.yml**
```yaml
postgres:
  image: postgis/postgis:16-3.4  # Cambiado a PostGIS para consistencia
  environment:
    POSTGRES_DB: monitoreo_dev         # ✅ Corregido
    POSTGRES_USER: monitoreo_user      # ✅ Corregido
    POSTGRES_PASSWORD: monitoreo_pass  # ✅ Corregido
  volumes:
    - ./database/init-data:/docker-entrypoint-initdb.d  # ✅ Scripts de inicialización
    - ./database/backups:/backups                        # ✅ Backups
    - ./database/scripts:/scripts                        # ✅ Scripts de gestión
  healthcheck:
    test: [ "CMD-SHELL", "pg_isready -U monitoreo_user -d monitoreo_dev" ]
```

### **2. Configuraciones ahora consistentes**

| Archivo | Usuario | Contraseña | Base de Datos |
|---------|---------|------------|---------------|
| `backend/app/core/config.py` | `monitoreo_user` | `monitoreo_pass` | `monitoreo_dev` |
| `docker-compose.yml` | `monitoreo_user` | `monitoreo_pass` | `monitoreo_dev` |
| `docker-compose.debug.yml` | `monitoreo_user` | `monitoreo_pass` | `monitoreo_dev` |

## 🚀 **Cómo aplicar la solución:**

### **Paso 1: Limpiar contenedores existentes**
```bash
# Detener y eliminar contenedores
docker-compose -f docker-compose.debug.yml down -v

# Limpiar volúmenes (⚠️ Esto elimina los datos)
docker volume prune -f

# Verificar que no queden contenedores
docker ps -a | grep vnm
```

### **Paso 2: Reconstruir entorno**
```bash
# Ejecutar task de VS Code para setup completo
# Ctrl+Shift+P → "Tasks: Run Task" → "Debug: Full Environment Setup"

# O manualmente:
docker-compose -f docker-compose.debug.yml up --build -d
```

### **Paso 3: Verificar conexión**
```bash
# Verificar que postgres esté funcionando
docker logs vnm_postgres_debug

# Probar conexión directa
docker exec vnm_postgres_debug pg_isready -U monitoreo_user -d monitoreo_dev

# Verificar que el backend se conecte
docker logs vnm_backend_debug
```

## 🧪 **Comandos de verificación:**

### **Verificar estado de contenedores:**
```bash
docker-compose -f docker-compose.debug.yml ps
```

### **Verificar logs de postgres:**
```bash
docker logs vnm_postgres_debug
```

### **Verificar logs de backend:**
```bash
docker logs vnm_backend_debug
```

### **Conectar manualmente a postgres:**
```bash
docker exec -it vnm_postgres_debug psql -U monitoreo_user -d monitoreo_dev
```

### **Verificar tablas creadas:**
```sql
-- Dentro de psql
\l                              -- Listar bases de datos
\c monitoreo_dev               -- Conectar a la base
\dn                            -- Listar esquemas
\dt seguridad.*                -- Listar tablas del esquema seguridad
SELECT COUNT(*) FROM seguridad.usuario;  -- Verificar datos
```

## 🔄 **Si aún hay problemas:**

### **1. Limpiar completamente:**
```bash
# Detener todo
docker-compose -f docker-compose.debug.yml down -v
docker-compose -f docker-compose.yml down -v

# Eliminar imágenes relacionadas
docker rmi $(docker images | grep vnm | awk '{print $3}')

# Limpiar system
docker system prune -f
```

### **2. Verificar puertos:**
```bash
# Verificar que puerto 5432 esté libre
netstat -an | grep 5432
# o
lsof -i :5432
```

### **3. Reconstruir desde cero:**
```bash
docker-compose -f docker-compose.debug.yml up --build --force-recreate
```

## 📁 **Archivos modificados:**
- ✅ `docker-compose.debug.yml` - Credenciales corregidas
- ✅ `SOLUCION_DATABASE_CREDENTIALS.md` - Este archivo de documentación

## 🎯 **Resultado esperado:**
Después de aplicar esta solución:
- ✅ Backend se conecta exitosamente a PostgreSQL
- ✅ Todas las tablas se crean automáticamente
- ✅ Datos iniciales se insertan correctamente
- ✅ API responde en `http://localhost:8000`
- ✅ Task `Fix Admin Password` funciona correctamente

## ⚠️ **Nota importante:**
Los volúmenes de datos se eliminan durante la limpieza. Si tenías datos importantes, asegúrate de hacer backup antes de aplicar la solución.
