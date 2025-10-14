# 🐞 Configuración de Debugging para VS Code con Docker

Esta guía te ayudará a configurar el debugging completo en VS Code para el proyecto VNM Monitoreo ejecutándose en contenedores Docker en Windows.

## 📋 Prerequisitos

1. **Docker Desktop** para Windows instalado y ejecutándose
2. **VS Code** con las extensiones recomendadas instaladas
3. **Git** para clonar el repositorio

## 🔧 Extensiones Requeridas

Las extensiones se instalarán automáticamente al abrir el proyecto. Revisa los archivos `.vscode/extensions.json` en cada carpeta.

### Para Backend (Python/FastAPI):
- Python
- Pylance  
- Docker
- Remote - Containers
- Thunder Client (para testing de APIs)
- autopep8 (formateador)

### Para Frontend (React/TypeScript):
- Prettier - Code formatter
- ESLint
- Auto Rename Tag
- Debugger for Chrome
- React Extension Pack
- TypeScript Importer

## 🚀 Configuración Paso a Paso

### 1. Abrir el Proyecto en VS Code

```bash
# Abrir desde la raíz del proyecto
code vnm-proyectos/
```

### 2. Opciones de Debugging Disponibles

#### 🎯 **Opción 1: Full Stack Debug (Recomendado)**
- **Configuración**: `🚀 Full Stack: Debug Both`
- **Descripción**: Debuggea backend y frontend simultáneamente
- **Pasos**:
  1. Ve a **Run and Debug** (Ctrl+Shift+D)
  2. Selecciona **"🚀 Full Stack: Debug Both"**
  3. Presiona **F5** - esto iniciará ambos debuggers

#### 🐍 **Opción 2: Solo Backend**
- **Configuración**: `🐍 Backend: FastAPI Docker Debug`
- **Descripción**: Debuggea solo el backend FastAPI en Docker
- **Puerto de debugging**: 5678

#### ⚛️ **Opción 3: Solo Frontend**
- **Configuración**: `⚛️ Frontend: React Chrome Debug`
- **Descripción**: Debuggea solo el frontend React en Chrome
- **URL**: http://localhost:3000

### 3. Iniciar el Entorno de Debugging

#### Método A: Usando Tasks de VS Code (Recomendado)
1. **Ctrl+Shift+P** → **"Tasks: Run Task"**
2. Seleccionar **"Docker: Start Debug Environment"**
3. Esperar a que todos los contenedores se inicien

#### Método B: Terminal Manual
```bash
# Desde la raíz del proyecto
docker-compose -f docker-compose.debug.yml up --build -d
```

### 5. Configuración de VS Code

#### ⚠️ Configuraciones Disponibles en `vscode-config/`
Las configuraciones de debugging están disponibles en la carpeta visible `vscode-config/` debido a que las carpetas `.vscode` no son visibles en la interfaz web.

#### 🚀 Instalación Automática (Recomendado)

**Windows:**
```powershell
.\setup-vscode-debug.ps1
```

**Linux/Mac:**
```bash
bash setup-vscode-debug.sh
```

#### 📋 Instalación Manual
Si los scripts no funcionan:
```bash
# Crear las carpetas
mkdir -p .vscode backend/.vscode frontend/.vscode

# Copiar configuraciones
cp vscode-config/root/* .vscode/
cp vscode-config/backend/* backend/.vscode/
cp vscode-config/frontend/* frontend/.vscode/
```

#### 📁 Configuraciones Incluidas

**📍 Raíz del Proyecto** (`vscode-config/root/` → `.vscode/`)
- **`launch.json`** - 7 configuraciones de debugging
- **`tasks.json`** - 13 tareas automatizadas  
- **`settings.json`** - Configuraciones del workspace
- **`extensions.json`** - Extensiones recomendadas

**🐍 Backend** (`vscode-config/backend/` → `backend/.vscode/`)
- **`launch.json`** - 4 configuraciones Python/FastAPI
- **`settings.json`** - Configuraciones Python
- **`extensions.json`** - Extensiones backend

**⚛️ Frontend** (`vscode-config/frontend/` → `frontend/.vscode/`)
- **`launch.json`** - 5 configuraciones React/Chrome
- **`settings.json`** - Configuraciones React/TypeScript
- **`extensions.json`** - Extensiones frontend

#### 📖 Documentación Completa
Revisa <filepath>vscode-config/README_CONFIGURACION_DEBUG.md</filepath> para instrucciones detalladas.
3. Seleccionar el contenedor `vnm_backend_debug`

#### Configuración de Breakpoints:
- Los breakpoints se pueden colocar en cualquier archivo `.py`
- El código se actualiza automáticamente con hot reload
- Los cambios en archivos se reflejan inmediatamente

### 3. Debugging del Frontend (React)

#### Para Chrome:
1. Asegúrate de que el frontend esté ejecutándose en `http://localhost:3000`
2. En VS Code, abre la carpeta `frontend`
3. Ve a **Run and Debug** (Ctrl+Shift+D)
4. Selecciona **"React: Launch Chrome"**
5. Presiona **F5**

#### Para Edge:
1. Selecciona **"React: Launch Edge"** en lugar de Chrome
2. Presiona **F5**

#### Debugging de Components:
- Coloca breakpoints en archivos `.jsx`, `.tsx`, `.js`, `.ts`
- El source mapping está configurado automáticamente
- Hot reload funciona con los breakpoints activos

## 🐛 Debugging de Problemas Específicos

### Verificar Logs en Tiempo Real:

```bash
# Backend logs
docker logs -f vnm_backend_debug

# Frontend logs  
docker logs -f vnm_frontend_debug

# Database logs
docker logs -f vnm_postgres_debug
```

## 🔍 Variables de Entorno para Debugging

### Backend (`docker-compose.debug.yml`):
```yaml
environment:
  - ENABLE_DEBUG=true      # Activa debugpy
  - DATABASE_URL=...       # Conexión a DB
  - SECRET_KEY=...         # JWT secret
```

### Frontend:
```yaml
environment:
  - VITE_API_URL=http://localhost:8000/api/v1
  - CHOKIDAR_USEPOLLING=true  # Hot reload en Windows
```

## 📂 Estructura de Configuraciones

```
vnm-proyectos/
├── backend/
│   ├── .vscode/
│   │   ├── launch.json       # Configuraciones de debug para Python
│   │   ├── settings.json     # Configuraciones del workspace
│   │   └── extensions.json   # Extensiones recomendadas
│   ├── Dockerfile.dev        # Docker con debugging habilitado
│   └── start-debug.py        # Script de inicio con opciones de debug
├── frontend/
│   ├── .vscode/
│   │   ├── launch.json       # Configuraciones de debug para React
│   │   ├── settings.json     # Configuraciones del workspace
│   │   └── extensions.json   # Extensiones recomendadas
│   └── Dockerfile.dev        # Docker para desarrollo
├── docker-compose.debug.yml  # Compose para debugging
└── DEBUG_SETUP.md           # Esta guía
```

## 🎯 Configuraciones de Launch específicas

### Backend - Python FastAPI:
- **Python: FastAPI Docker Attach**: Conecta al contenedor Docker
- **Python: FastAPI Local Debug**: Ejecuta localmente (sin Docker)
- **Python: Debug Current File**: Debug del archivo actual
- **Python: Run Tests**: Ejecutar tests con debugging

### Frontend - React:
- **React: Launch Chrome**: Abre Chrome con debugging
- **React: Attach to Chrome**: Se conecta a Chrome existente
- **React: Launch Edge**: Abre Edge con debugging
- **React: Run Tests**: Ejecutar tests de React

## 🔧 Solución de Problemas Comunes

### 1. "Cannot connect to Docker daemon"
```bash
# Verificar que Docker Desktop esté ejecutándose
docker version
```

### 2. "Port already in use"
```bash
# Detener contenedores existentes
docker-compose -f docker-compose.debug.yml down
```

### 3. "Debugger not connecting"
- Verificar que el puerto 5678 esté expuesto
- Reiniciar el contenedor backend
- Verificar firewall de Windows

### 4. "Hot reload not working"
- Verificar variable `CHOKIDAR_USEPOLLING=true`
- Reiniciar contenedor frontend

## 📝 Tips Adicionales

1. **Usar Thunder Client**: Para probar endpoints de API directamente desde VS Code
2. **Git Integration**: GitLens está incluido para mejor integración con Git
3. **Code Formatting**: Prettier y Black se ejecutan automáticamente al guardar
4. **Type Checking**: Pylance y TypeScript proporcionan checking en tiempo real

## 🔄 Comandos Útiles

```bash
# Iniciar en modo debug
docker-compose -f docker-compose.debug.yml up

# Reconstruir y iniciar
docker-compose -f docker-compose.debug.yml up --build

# Detener todo
docker-compose -f docker-compose.debug.yml down

# Ver logs en tiempo real
docker-compose -f docker-compose.debug.yml logs -f

# Entrar al contenedor backend
docker exec -it vnm_backend_debug bash

# Entrar al contenedor frontend  
docker exec -it vnm_frontend_debug sh
```

¡Ahora tienes un entorno de desarrollo completamente configurado para debugging!
