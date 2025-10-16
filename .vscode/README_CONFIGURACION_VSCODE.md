# Configuracion VS Code - Ambiente Virtual Simplificado

## Archivos Configurados Correctamente

### ✅ settings.json - PERFECTO
- Ambiente virtual Python: `.venv/Scripts/python.exe`
- Auto-activacion de terminal
- Formato automatico (Black para Python, Prettier para JS)
- Linting habilitado (Flake8 + ESLint)
- Configuraciones cross-platform

### ✅ launch.json - CORREGIDO
**Nuevas configuraciones de debugging:**

1. **Backend Debug (Local)** - Ejecuta FastAPI localmente
2. **Backend Debug (Container)** - Se conecta a container Docker  
3. **Frontend Debug** - Abre Chrome/Edge con debugging habilitado
4. **FullStack Debug** - Inicia containers + backend local

### ✅ tasks.json - COMPLETAMENTE RENOVADO
**Nuevas tareas disponibles:**

- `start-containers` - Usar docker_manager.py
- `start-containers-debug` - Modo debug con containers
- `stop-containers` - Detener containers
- `start-frontend` - npm run dev
- `install-python-dependencies` - pip install desde .venv
- `install-frontend-dependencies` - npm install
- `activate-venv` - Activar ambiente virtual
- `docker-status` - Ver estado de containers
- `run-diagnostics` - Ejecutar diagnostico del sistema

### ✅ extensions.json - PERFECTO
Lista completa de extensiones recomendadas para fullstack.

## Como Usar el Debugging

### 1. Debugging Local del Backend

**Usar cuando:** Quieres depurar sin containers

1. Iniciar PostgreSQL: `python docker_manager.py start` (solo BD)
2. En VS Code: F5 -> "Backend Debug (Local)"
3. Breakpoints funcionan directamente

### 2. Debugging Frontend  

**Usar cuando:** Problemas en React/JavaScript

1. F5 -> "Frontend Debug"
2. Abre automáticamente el navegador con DevTools conectado
3. Breakpoints en código TypeScript/JavaScript

### 3. Debugging FullStack

**Usar cuando:** Quieres depurar todo el stack

1. F5 -> "FullStack Debug"
2. Inicia containers automáticamente
3. Luego inicia backend local
4. Frontend se ejecuta separadamente

### 4. Debugging con Containers

**Usar cuando:** Problemas específicos del entorno containerizado

1. `python docker_manager.py start-debug`
2. F5 -> "Backend Debug (Container)"
3. Se conecta al puerto 5678 del container

## Tareas Utiles

**Acceso rapido con Ctrl+Shift+P:**

- "Tasks: Run Task" -> Seleccionar tarea
- "Tasks: start-containers" - Iniciar Docker
- "Tasks: stop-containers" - Detener Docker
- "Tasks: run-diagnostics" - Verificar sistema

## Comandos de Terminal Integrado

**VS Code detecta automáticamente el ambiente virtual:**

```bash
# Al abrir terminal, se activa automáticamente .venv
# Comandos disponibles:
python --version              # Verifica Python del .venv
pip list                      # Paquetes instalados
python docker_manager.py      # Manejar containers
cd frontend && npm run dev     # Iniciar frontend
```

## Configuraciones Importantes

### Python
- **Intérprete:** `.venv/Scripts/python.exe` 
- **Formato:** Black (automático al guardar)
- **Linting:** Flake8 habilitado
- **Auto-import:** Organizar imports al guardar

### Frontend
- **ESLint:** Configurado para directorio frontend
- **TypeScript:** Imports relativos preferidos
- **Emmet:** Habilitado para JSX

### Debugging
- **Breakpoints:** Habilitados en todas partes
- **JustMyCode:** Deshabilitado (permite depurar librerías)
- **Puerto Backend:** 8000 (local) y 5678 (container debug)
- **Puerto Frontend:** 3000

## Problemas Solucionados

1. ❌ **launch.json usaba rutas incorrectas** -> ✅ Corregido con uvicorn
2. ❌ **tasks.json referenciaba scripts eliminados** -> ✅ Usa docker_manager.py
3. ❌ **Debugging solo para containers** -> ✅ Agregado debugging local  
4. ❌ **Tareas obsoletas** -> ✅ Tareas simplificadas y funcionales

## Verificacion

Para verificar que todo funciona:

1. **Abrir VS Code:** `code .`
2. **Ver intérprete:** Ctrl+Shift+P -> "Python: Select Interpreter" 
3. **Ejecutar tarea:** Ctrl+Shift+P -> "Tasks: Run Task" -> "run-diagnostics"
4. **Probar debugging:** F5 -> Seleccionar configuración

**Todo debe funcionar sin errores con la nueva estructura simplificada.**