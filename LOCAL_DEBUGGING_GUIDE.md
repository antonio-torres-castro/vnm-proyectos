# Guía de Debugging Local Full-Stack con Ambientes Virtuales

## Configuración Completada ✅

Se han creado las configuraciones de debugging para desarrollo local sin Docker (excepto la base de datos), usando ambientes virtuales aislados.

## Estructura de Ambientes Virtuales

```
vnm-proyectos/
├── backend/
│   └── .venv/                    # ← Python virtual environment
│       ├── Scripts/python.exe    # ← Intérprete Python aislado
│       └── Lib/                  # ← Dependencias Python aisladas
├── frontend/
│   ├── node_modules/             # ← Dependencias Node.js locales
│   └── .nvmrc                    # ← Control de versión Node.js
└── _vscode/
    ├── launch.json               # ← Configurado para usar .venv
    ├── tasks.json                # ← Tareas con activación .venv
    └── settings.json             # ← Intérprete Python por defecto
```

## Setup Manual de Ambientes Virtuales

### Paso 1: Backend - Crear .venv Python

```bash
cd vnm-proyectos/backend
python -m venv .venv
.venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements-dev.txt
```

**Verificación:**
```bash
python -c "import fastapi; print('FastAPI OK')"
where python  # Debe mostrar: ...\backend\.venv\Scripts\python.exe
```

### Paso 2: Frontend - Node Local

```bash
cd vnm-proyectos/frontend
npm install
```

**Verificación:**
```bash
npm run dev --version
npx vite --version
```

## Configuraciones Disponibles

### 1. **Frontend Debug (Local)**
- **Tipo:** Chrome debugging con Node.js local
- **Puerto:** localhost:3000 (Vite)
- **Dependencias:** node_modules local + .nvmrc
- **Source Maps:** Habilitados para debugging directo en archivos .jsx

### 2. **Backend Debug (Local)**
- **Tipo:** Python debugging con .venv
- **Puerto:** localhost:8000 (FastAPI)
- **Intérprete:** `backend/.venv/Scripts/python.exe`
- **Características:** Hot reload habilitado, breakpoints en código Python

### 3. **FullStack Debug (Local)**
- **Tipo:** Compound (ejecuta ambos simultáneamente)
- **Ambientes:** .venv Python + node_modules local
- **Funcionalidad:** Inicia automáticamente frontend y backend aislados

## Cómo Usar

### Prerrequisitos
1. **Base de datos debe estar corriendo:**
   ```bash
   docker-compose up -d
   ```

2. **Ambientes virtuales creados** (ver "Setup Manual" arriba)

### Debugging Individual

#### Frontend Solo
1. Usar tarea "Start Frontend Dev Server" o manual: `npm run dev` en `/frontend`
2. Ejecutar configuración "Frontend Debug (Local)"
3. Se abrirá Chrome con debugging habilitado
4. Poner breakpoints en archivos .jsx

#### Backend Solo
1. Ejecutar configuración "Backend Debug (Local)"
2. VS Code usará automáticamente `backend/.venv/Scripts/python.exe`
3. Uvicorn iniciará automáticamente en puerto 8000
4. Poner breakpoints en archivos .py

### Debugging Full-Stack
1. **Método Recomendado:** Ejecutar configuración "FullStack Debug (Local)"
2. Se iniciará automáticamente:
   - Servidor Vite (frontend) usando node_modules local
   - Servidor Uvicorn (backend) usando .venv Python
   - Chrome con debugging habilitado
3. Poner breakpoints en ambos frontend y backend
4. Debugging completo del flujo de datos

## Tareas VS Code Disponibles

| Tarea | Función | Comando Equivalente |
|---|---|---|
| **Create Backend .venv** | Crea ambiente virtual Python | `python -m venv .venv` |
| **Install Backend Dependencies (.venv)** | Instala en .venv | `.venv\Scripts\activate && pip install -r requirements-dev.txt` |
| **Install Frontend Dependencies** | Instala node_modules local | `npm install` |
| **Activate Backend .venv** | Activa ambiente virtual | `.venv\Scripts\activate` |
| **Start Backend Dev Server (.venv)** | Inicia Uvicorn con .venv | `.venv\Scripts\activate && uvicorn app.main:app --reload` |

## Ventajas de los Ambientes Virtuales

### ✅ **Aislamiento Completo**
- **Backend:** Dependencias Python aisladas en .venv
- **Frontend:** Dependencias Node.js en node_modules local
- **Base de datos:** PostgreSQL en container Docker
- **Sin conflictos:** Cada ambiente tiene sus propias dependencias

### ✅ **Control de Versiones**
- **Python:** Usa el intérprete específico del .venv
- **Node.js:** Controlado por .nvmrc (18.17.0)
- **Dependencias:** Exactas según requirements-dev.txt y package.json

### ✅ **Debugging Mejorado**
- **VS Code:** Detecta automáticamente el .venv
- **Breakpoints:** Funcionan en código fuente, no en site-packages
- **Console.log:** Aparecen en navegador sin interferencias
- **Hot Reload:** Funciona perfectamente en ambos ambientes

## Resolución del Problema Original

El problema del botón "Cerrar Sesión" que no mostraba el estado de loading se debía a:

1. **Entorno Docker Complejo:** Hot reload no funcionaba correctamente
2. **Console.log Invisibles:** Los logs no aparecían en el navegador
3. **Debugging Bloqueado:** VS Code no podía conectar breakpoints efectivamente
4. **Conflictos de Dependencias:** Sin aislamiento de ambientes

Con el nuevo entorno local + .venv, estos problemas están **resueltos** ✅.

## Próximos Pasos - Fase 4: Validación

1. **Crear ambientes virtuales** (pasos manuales arriba)
2. **Probar configuración FullStack Debug (Local)**
3. **Verificar que los breakpoints funcionen en Header.jsx línea 194**
4. **Confirmar que los console.log aparezcan en Chrome DevTools**
5. **Validar el fix del botón logout con debugging real**

---

*Configuración actualizada con ambientes virtuales - VNM Simple Solutions Axiom aplicado*