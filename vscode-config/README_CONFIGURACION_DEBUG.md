# 🔧 Configuración de Debugging para VS Code

## 📖 Descripción

Esta configuración provee un entorno completo de debugging para el proyecto VNM con soporte para:
- **Backend FastAPI** con debugging remoto via Docker
- **Frontend React** con debugging en Edge/Chrome
- **Tareas automatizadas** para gestión del entorno
- **Extensiones optimizadas** para desarrollo

## 📁 Estructura de Archivos

```
vscode-config/
├── root/
│   ├── launch.json     # 5 configuraciones React/Edge + Chrome
│   ├── tasks.json      # 18 tareas automatizadas
│   └── extensions.json # Extensiones backend+frontend
├── backend/
│   ├── launch.json     # 5 configuraciones Python
│   └── settings.json   # Configuración Python/Flask8
└── frontend/
    ├── launch.json     # 6 configuraciones React
    └── extensions.json # Extensiones frontend
```

## 🚀 Instalación Rápida

### Windows (PowerShell)
```powershell
# Desde la raíz del proyecto vnm-proyectos
./setup-vscode-debug.ps1
```

### Linux/Mac (Bash)
```bash
# Desde la raíz del proyecto vnm-proyectos
bash setup-vscode-debug.sh
```

## 📋 Instalación Manual

Si los scripts no funcionan, puedes copiar manualmente:

### 1. Crear las carpetas
```bash
mkdir -p .vscode
mkdir -p backend/.vscode  
mkdir -p frontend/.vscode
```

### 2. Copiar los archivos
```bash
# Raíz del proyecto
cp vscode-config/root/* .vscode/

# Backend
cp vscode-config/backend/* backend/.vscode/

# Frontend  
cp vscode-config/frontend/* frontend/.vscode/
```

## 🎯 Configuraciones de Debug Disponibles

### 🚀 **Full Stack: Debug Both**
- **Descripción**: Debuggea backend + frontend simultáneamente
- **Componentes**: FastAPI Docker + React Edge
- **Uso**: Debugging completo del sistema

### 🐍 **Backend: FastAPI Docker Debug**
- **Descripción**: Debuggea el backend via Docker
- **Puerto**: 5678 (debugpy)
- **Requisito**: Contenedor backend ejecutándose

### 🌐 **Frontend: React Edge Debug (Principal)**
- **Descripción**: Debuggea React con Microsoft Edge
- **Puerto**: 3000
- **Ventaja**: Mejor integración con herramientas modernas
- **Recomendado**: Opción principal para debugging

### 🔧 **Frontend: Edge DevTools (Avanzado)**
- **Descripción**: Debugging avanzado con DevTools integrado
- **Puerto**: 3000
- **Características**: DevTools completo dentro de VS Code

### ⚛️ **Frontend: Attach to Edge**
- **Descripción**: Se conecta a Edge existente
- **Puerto**: 9222
- **Uso**: Para debugging de sesiones ya abiertas

### 🔧 **Frontend: Chrome (Alternativo)**
- **Descripción**: Debuggea React con Chrome (opción secundaria)
- **Puerto**: 3000
- **Uso**: Si Edge no está disponible

### 🐍 **Backend: Local Python Debug**
- **Descripción**: Debuggea backend sin Docker
- **Uso**: Para desarrollo local directo

### 🧪 **Tests con Debugging**
- **Backend**: Ejecuta pytest con debugging
- **Frontend**: Ejecuta tests React con debugging

## 🔧 Tareas Automatizadas Incluidas

### Docker Management
- **Start Debug Environment** - Inicia todo el entorno
- **Stop Debug Environment** - Detiene todo el entorno  
- **Start Backend Debug Container** - Solo backend
- **Start Frontend Dev Server** - Solo frontend

### Development
- **Install Dependencies** - Backend y frontend
- **Run Tests** - Backend y frontend
- **View Logs** - Para cada servicio

## 🚀 Guía de Uso Rápida

### 1. Configurar VS Code
```bash
# En la raíz del proyecto
code .

# O ejecutar el script de setup
./setup-vscode-debug.ps1  # Windows
bash setup-vscode-debug.sh  # Linux/Mac
```

### 2. Instalar Extensiones
VS Code te sugerirá instalar las extensiones recomendadas automáticamente.

**📱 Extensiones Principales (Frontend)**:
- **Microsoft Edge DevTools** (`ms-edgedevtools.vscode-edge-devtools`) - 🌟 **Principal** para debugging React
- **ESLint** - Análisis de código JavaScript/TypeScript
- **Prettier** - Formateo automático de código
- **React Snippets** - Acelera desarrollo React

**🐍 Extensiones Principales (Backend)**:
- **Python** - Soporte completo Python
- **Python Debugger** - Debugging específico Python
- **Pylint** - Análisis de código Python

> ✅ **Configuración Moderna**: Edge como navegador principal, Chrome como alternativa. Se removió la extensión deprecada `Debugger for Chrome`.

### 3. Iniciar Entorno de Debugging

**🌟 Opciones Recomendadas (en orden de prioridad):**
1. **`🚀 Full Stack: Debug Both`** - Debuggea backend + frontend con Edge
2. **`⚛️ Frontend: React Edge Debug (Principal)`** - Solo frontend con Edge
3. **`🔧 Frontend: Edge DevTools (Avanzado)`** - DevTools integrado en VS Code
4. **`🔧 Frontend: Chrome (Alternativo)`** - Solo si Edge no está disponible

**📋 Pasos:**
- `Ctrl+Shift+D` (Run and Debug)
- Seleccionar la configuración deseada
- Presionar `F5`

**Opción A**: Usar Task de VS Code
- `Ctrl+Shift+P` → `Tasks: Run Task` → `Docker: Start Debug Environment`

**Opción B**: Terminal
```bash
docker-compose -f docker-compose.debug.yml up -d
```

## 🔍 Verificación

Después de la instalación, verifica que existan estos archivos:
- `.vscode/launch.json`
- `.vscode/tasks.json`
- `.vscode/settings.json`
- `.vscode/extensions.json`
- `backend/.vscode/launch.json`
- `backend/.vscode/settings.json`
- `frontend/.vscode/launch.json`
- `frontend/.vscode/extensions.json`

## 🆘 Resolución de Problemas

### Problema: Admin no puede hacer login
**Solución**: Usar las credenciales correctas:
- Email: `admin@monitoreo.cl`
- Password: `admin123`

### Problema: Debugging no conecta
**Verificar**:
1. Contenedores ejecutándose: `docker-compose -f docker-compose.debug.yml ps`
2. Puerto 5678 libre: `netstat -an | grep 5678`
3. Firewall no bloqueando puertos

### Problema: Frontend no inicia
**Verificar**:
1. Node.js instalado: `node --version`
2. Dependencies instaladas: `npm install` en /frontend
3. Puerto 3000 libre

## 🔧 Personalización

### Cambiar puertos
Edita `docker-compose.debug.yml` y actualiza los launch configs correspondientes.

### Agregar extensiones
Edita los `extensions.json` en cada directorio según necesites.

### Modificar tareas
Edita `tasks.json` para agregar o modificar comandos automatizados.

---

## 📞 Soporte

Si encuentras problemas con esta configuración, verifica:
1. Versión de VS Code actualizada
2. Extensiones Python y Edge DevTools instaladas
3. Docker Desktop ejecutándose
4. Puertos no ocupados por otros servicios

¡Happy Debugging! 🐛✨
