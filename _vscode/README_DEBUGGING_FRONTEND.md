# Guía de Debugging Frontend + Backend

## Configuraciones de Debugging Disponibles

### 1. FullStack Debug (Complete) ⭐ **RECOMENDADO**
- **Qué hace**: Debuggea BACKEND + FRONTEND simultáneamente
- **Cuándo usar**: Para debugging completo del stack
- **Breakpoints**: ✅ Backend (Python) + ✅ Frontend (React/JS)

### 2. FullStack Debug (Smart)
- **Qué hace**: Solo debuggea BACKEND
- **Cuándo usar**: Solo para debugging de API/backend
- **Breakpoints**: ✅ Backend (Python) solamente

### 3. Frontend Debug (Container)
- **Qué hace**: Solo debuggea FRONTEND
- **Cuándo usar**: Solo para debugging de React/JS
- **Breakpoints**: ✅ Frontend (React/JS) solamente

## Instrucciones de Uso

### Para Debugging Completo (Backend + Frontend):
1. **Usar**: `FullStack Debug (Complete)`
2. **Resultado**: 
   - Los breakpoints en archivos `.py` (backend) se pondrán rojos y funcionarán
   - Los breakpoints en archivos `.jsx/.js` (frontend) se pondrán rojos y funcionarán
   - Se abrirá una nueva ventana de Edge/Chrome para el frontend

### Solución de Problemas

#### ❌ "Los breakpoints del frontend no se ponen rojos"
**Causa**: Usando `FullStack Debug (Smart)` en lugar de `FullStack Debug (Complete)`
**Solución**: Cambiar a `FullStack Debug (Complete)`

#### ❌ "Error al conectar al frontend"
**Causa**: Los contenedores no están completamente listos
**Solución**: 
1. Esperar 30-60 segundos después de iniciar
2. Verificar que http://localhost:3000 responda en el navegador
3. Reiniciar el debugging

#### ❌ "Source maps no se cargan"
**Causa**: Configuración de Vite
**Solución**: Ya está optimizada en `vite.config.js`

## Archivos Configurados

- ✅ `.vscode/launch.json`: Configuraciones de debugging
- ✅ `frontend/vite.config.js`: Source maps optimizados
- ✅ `docker-compose.debug.yml`: Puertos expuestos correctamente

## Puertos de Debugging

- **Backend**: `localhost:5678` (debugger Python)
- **Frontend**: `localhost:3000` (aplicación React)
- **API**: `localhost:8000` (FastAPI docs)
- **PgAdmin**: `localhost:5050` (base de datos)