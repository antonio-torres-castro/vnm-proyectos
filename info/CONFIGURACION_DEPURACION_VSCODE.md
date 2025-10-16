# Configuración de Depuración VS Code

## Configuraciones Disponibles

Se han configurado tres modos de depuración para el proyecto:

### 1. Frontend Debug
- **Propósito**: Depurar solo la aplicación React
- **Puerto**: localhost:3000
- **Prerequisitos**: 
  - Extensión "Debugger for Chrome" instalada
  - Dependencias del frontend instaladas (`npm install` en /frontend)

### 2. Backend Debug
- **Propósito**: Depurar solo la API FastAPI
- **Puerto**: localhost:8000
- **Prerequisitos**:
  - Extensión "Python" instalada
  - Entorno virtual Python activado
  - Servicios de base de datos iniciados (PostgreSQL, Redis)

### 3. FullStack Debug
- **Propósito**: Depurar frontend y backend simultáneamente
- **Tipo**: Configuración compuesta
- **Prerequisitos**: Todos los anteriores

## Cómo Usar

### Opción 1: Panel de Depuración
1. Abre el panel de depuración (Ctrl+Shift+D)
2. Selecciona la configuración deseada en el dropdown
3. Presiona F5 o el botón de play verde

### Opción 2: Comando Rápido
1. Presiona Ctrl+Shift+P
2. Escribe "Debug: Select and Start Debugging"
3. Selecciona la configuración deseada

### Opción 3: F5 Directo
1. Presiona F5
2. Si es la primera vez, VS Code te pedirá seleccionar una configuración
3. Elige "FullStack Debug" para depurar todo el stack

## Tareas Automatizadas

Las configuraciones incluyen tareas automatizadas que se ejecutan antes del inicio:

- **start-frontend**: Inicia el servidor de desarrollo de React
- **start-backend-dependencies**: Inicia PostgreSQL y Redis usando Docker
- **start-fullstack-environment**: Inicia todo el entorno de desarrollo

## Puntos de Interrupción

### Frontend (React/TypeScript)
- Coloca breakpoints directamente en archivos .ts/.tsx
- La depuración funciona gracias a los source maps

### Backend (Python)
- Coloca breakpoints en archivos .py
- Variables locales y stack trace disponibles
- Hot reload habilitado para cambios en código

## Solución de Problemas

### Error: "Attribute 'request' is missing"
✅ **SOLUCIONADO**: Se ha corregido la configuración de launch.json

### Error: "Cannot connect to Chrome"
- Verifica que la extensión "Debugger for Chrome" esté instalada
- Asegúrate de que Chrome esté cerrado antes de iniciar la depuración

### Error: "Python interpreter not found"
- Configura el intérprete de Python: Ctrl+Shift+P > "Python: Select Interpreter"
- Selecciona el intérprete del entorno virtual: `./.venv/bin/python`

### Error: "Database connection failed"
- Ejecuta manualmente: `python devtools/orquestador_desarrollo.py iniciar`
- Verifica que Docker esté ejecutándose

## Extensiones Recomendadas

VS Code sugerirá automáticamente instalar las extensiones necesarias.
Puedes instalarlas manualmente desde la pestaña de extensiones:

- Python
- Debugger for Chrome
- Prettier
- Tailwind CSS
- Black Formatter
- Flake8

## Configuración de Entorno

### Variables de Entorno
- `PYTHONPATH`: Configurado automáticamente para el backend
- `ENVIRONMENT`: Establecido en "development"

### Rutas de Trabajo
- Frontend: `${workspaceFolder}/frontend`
- Backend: `${workspaceFolder}/backend`

---

**Próximos pasos**: Reinicia VS Code para que las configuraciones tomen efecto, luego prueba presionar F5 y seleccionar "FullStack Debug".
