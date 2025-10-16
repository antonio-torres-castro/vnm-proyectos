# Extensiones VS Code Optimizadas para VNM Project

Este documento contiene las extensiones VS Code específicas y optimizadas para nuestro stack tecnológico actual, basado en una auditoría completa del proyecto.

## Stack Tecnológico Identificado

**Backend:**
- FastAPI (Python web framework)
- SQLAlchemy (ORM)
- PostgreSQL/PostGIS (base de datos geoespacial)
- Pydantic (validación)
- JWT Authentication (python-jose)
- Remote debugging con debugpy

**Frontend:**
- React 18 con JSX
- TypeScript
- Vite (build tool)
- React Router DOM
- Axios (HTTP client)
- CSS personalizado

**DevOps:**
- Docker/Docker Compose
- VS Code remote debugging
- Hot reload development

---

## EXTENSIONES ESENCIALES (Core)

### Python/Backend (Obligatorias)
```json
"ms-python.python"              // Python extension pack
"ms-python.debugpy"             // Python debugger (remote debugging)
```

### JavaScript/TypeScript/React (Obligatorias)
```json
"ms-vscode.vscode-typescript-next"     // TypeScript support
"bradlc.vscode-tailwindcss"            // CSS IntelliSense (si usamos Tailwind)
```

### Debugging (Obligatorias)
```json
"ms-vscode.js-debug"            // JavaScript debugger
"ms-edgedevtools.vscode-edge-devtools"  // Browser debugging tools
```

---

## EXTENSIONES RECOMENDADAS (Quality of Life)

### Formateo y Linting
```json
"ms-python.black-formatter"     // Python code formatter
"ms-python.isort"              // Python import sorter
"esbenp.prettier-vscode"       // JavaScript/TypeScript formatter
"ms-python.flake8"             // Python linting
"dbaeumer.vscode-eslint"       // JavaScript/TypeScript linting
```

### React Development
```json
"dsznajder.es7-react-js-snippets"      // React snippets
"formulahendry.auto-rename-tag"        // Auto rename paired HTML/JSX tags
"bradlc.vscode-tailwindcss"            // Tailwind CSS IntelliSense
```

### Database & SQL
```json
"ckolkman.vscode-postgres"      // PostgreSQL support
"mtxr.sqltools"                // SQL tools
"mtxr.sqltools-driver-pg"      // PostgreSQL driver for SQLtools
```

### Docker & DevOps
```json
"ms-azuretools.vscode-docker"   // Docker container management
"ms-vscode-remote.remote-containers" // Dev containers support
```

---

## EXTENSIONES OPCIONALES (Nice to Have)

### Git & Version Control
```json
"eamodio.gitlens"              // Git supercharged
"github.vscode-pull-request-github" // GitHub integration
```

### Productivity
```json
"gruntfuggly.todo-tree"        // TODO/FIXME highlighting
"aaron-bond.better-comments"   // Enhanced comments
"usernamehw.errorlens"         // Inline error display
"visualstudioexptteam.vscodeintellicode" // AI-assisted coding
```

### Files & Navigation
```json
"ms-vscode.vscode-json"        // JSON support
"redhat.vscode-yaml"           // YAML support
"vscode-icons-team.vscode-icons" // File icons
```

### API Development
```json
"rangav.vscode-thunder-client"  // REST API client (alternative to Postman)
"humao.rest-client"            // HTTP REST client
```

---

## CONFIGURACIONES ESPECÍFICAS RECOMENDADAS

### Para Python (settings.json)
```json
{
    "python.defaultInterpreterPath": "./.venv/Scripts/python.exe",
    "python.terminal.activateEnvironment": true,
    "python.analysis.typeCheckingMode": "basic",
    "python.linting.enabled": true,
    "python.linting.flake8Enabled": true,
    "python.linting.pylintEnabled": false,
    "python.formatting.provider": "black"
}
```

### Para TypeScript/React (settings.json)
```json
{
    "eslint.workingDirectories": ["frontend"],
    "typescript.preferences.importModuleSpecifier": "relative",
    "emmet.includeLanguages": {
        "javascript": "javascriptreact"
    },
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
        "source.organizeImports": "explicit"
    }
}
```

### Para Debugging (settings.json)
```json
{
    "debug.allowBreakpointsEverywhere": true,
    "debug.showInlineBreakpointCandidates": true,
    "debug.showBreakpointsInOverviewRuler": true
}
```

---

## EXTENSIONES A EVITAR (Conflictos Conocidos)

### Evitar duplicación de funcionalidad:
- ❌ **Pylint** (si ya usas Flake8)
- ❌ **Multiple Python formatters** (elegir solo Black)
- ❌ **ESLint duplicados** (una sola configuración)
- ❌ **Prettier conflicting formatters**

### Extensiones problemáticas para nuestro stack:
- ❌ **Auto Import - ES6, TS, JSX, TSX** (puede conflictuar con TypeScript nativo)
- ❌ **Python Docstring Generator** (si ya tienes autoDocstring)
- ❌ **Bracket Pair Colorizer** (VS Code ya lo incluye nativamente)

---

## INSTALACIÓN AUTOMÁTICA

Usar el script automatizado:
```bash
python automate/instalar_extensiones_vscode.py
```

O instalar manualmente las esenciales:
```bash
code --install-extension ms-python.python
code --install-extension ms-python.debugpy
code --install-extension ms-vscode.vscode-typescript-next
code --install-extension ms-vscode.js-debug
code --install-extension ms-edgedevtools.vscode-edge-devtools
```

---

## VALIDACIÓN DE EXTENSIONES

Para verificar que todas las extensiones funcionan correctamente:
```bash
python automate/validar_extensiones_vscode.py
```

---

## NOTAS IMPORTANTES

1. **Orden de instalación:** Instalar primero las extensiones esenciales, luego las recomendadas
2. **Conflictos:** Si experimentas lentitud, desactiva extensiones opcionales una por una
3. **Workspace settings:** Las configuraciones están optimizadas para workspace, no user settings
4. **Updates:** Mantener extensiones actualizadas para mejor compatibilidad
5. **Performance:** Deshabilitar extensiones no utilizadas en este proyecto específico

---

## CONFIGURACIÓN POR DIRECTORIO

### Workspace Root (vnm-proyectos/)
- Extensiones de Git y productividad general
- Docker y contenedores
- Extensiones de archivos (JSON, YAML)

### Backend Directory (vnm-proyectos/backend/)
- Todas las extensiones de Python
- Database tools
- API development tools

### Frontend Directory (vnm-proyectos/frontend/)
- TypeScript y React extensions
- CSS tools
- Browser debugging tools

Esta configuración está optimizada específicamente para nuestro stack y ha sido probada para evitar conflictos entre extensiones.