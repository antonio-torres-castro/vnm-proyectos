# 🐞 Configuraciones de Debugging para VS Code

## ⚠️ Problema Identificado
Las carpetas `.vscode` no son visibles en la interfaz web debido a que el sistema filtra archivos/carpetas que comienzan con punto (`.`).

## ✅ Solución Implementada
Las configuraciones están disponibles en esta carpeta `vscode-config/` que es visible en la interfaz web.

## 📁 Estructura de Configuraciones

```
vscode-config/
├── root/           # Configuraciones para la raíz del proyecto (.vscode/)
│   ├── launch.json     # 7 configuraciones de debugging
│   ├── tasks.json      # 13 tareas automatizadas
│   ├── settings.json   # Configuraciones del workspace
│   └── extensions.json # Extensiones recomendadas
├── backend/        # Configuraciones para backend/ (.vscode/)
│   ├── launch.json     # 4 configuraciones Python/FastAPI
│   ├── settings.json   # Configuraciones Python
│   └── extensions.json # Extensiones backend
└── frontend/       # Configuraciones para frontend/ (.vscode/)
    ├── launch.json     # 5 configuraciones React/Edge + Chrome
    ├── settings.json   # Configuraciones React/TypeScript
    └── extensions.json # Extensiones frontend
```

## 🚀 Instalación Automática

### Windows (PowerShell)
```powershell
# Desde la raíz del proyecto vnm-proyectos
.\setup-vscode-debug.ps1
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

## 🎯 Configuraciones de Debugging Disponibles

### 🚀 **Full Stack: Debug Both**
- **Descripción**: Debuggea backend y frontend simultáneamente
- **Uso**: Ideal para desarrollo completo
- **Puertos**: Backend 5678, Frontend 3000

### 🐍 **Backend: FastAPI Docker Debug**
- **Descripción**: Debuggea solo el backend en Docker
- **Puerto**: 5678
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

### Login Fix
- **Fix Admin Password** - ⭐ **Soluciona el problema de login**
- **Debug: Test Login API** - Prueba la autenticación

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
**Opción A**: Usar Task de VS Code
- `Ctrl+Shift+P` → `Tasks: Run Task` → `Docker: Start Debug Environment`

**Opción B**: Terminal
```bash
docker-compose -f docker-compose.debug.yml up -d
```

### 4. Arreglar Login del Administrador
**Opción A**: Usar Task de VS Code
- `Ctrl+Shift+P` → `Tasks: Run Task` → `Fix Admin Password`

**Opción B**: Terminal
```bash
curl -X POST http://localhost:8000/api/v1/auth/fix-admin-password \
  -H "accept: application/json" \
  -H "Content-Type: application/json"
```

### 5. Iniciar Debugging

**🌟 Opciones Recomendadas (en orden de prioridad):**
1. **`🚀 Full Stack: Debug Both`** - Debuggea backend + frontend con Edge
2. **`⚛️ Frontend: React Edge Debug (Principal)`** - Solo frontend con Edge
3. **`🔧 Frontend: Edge DevTools (Avanzado)`** - DevTools integrado en VS Code
4. **`🔧 Frontend: Chrome (Alternativo)`** - Solo si Edge no está disponible

**📋 Pasos:**
- `Ctrl+Shift+D` (Run and Debug)
- Seleccionar la configuración deseada
- Presionar `F5`

## 🔍 Verificación

Después de la instalación, verifica que existan estos archivos:
- `.vscode/launch.json`
- `.vscode/tasks.json`
- `.vscode/settings.json`
- `.vscode/extensions.json`
- `backend/.vscode/launch.json`
- `backend/.vscode/settings.json`
- `frontend/.vscode/launch.json`
- `frontend/.vscode/settings.json`

## 🐛 Troubleshooting

### Problema: Carpetas .vscode no visibles
- **Causa**: Filtro de archivos ocultos en la interfaz web
- **Solución**: Usar los scripts de setup o copia manual

### Problema: Error al conectar debugger
- **Causa**: Contenedores no iniciados o puertos ocupados
- **Solución**: Verificar `docker-compose ps` y reiniciar contenedores

### Problema: Login falla después del debug setup
- **Causa**: Hash de password incorrecto en la base de datos
- **Solución**: Ejecutar tarea `Fix Admin Password`

## 📞 Soporte

Para más detalles, revisa:
- `DEBUG_SETUP.md` - Guía completa de debugging
- `docker-compose.debug.yml` - Configuración Docker
- `backend/start-debug.py` - Script de inicio del backend
