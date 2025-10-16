# Extensiones Recomendadas para VS Code - VNM Proyectos

Este documento lista las extensiones recomendadas para trabajar eficientemente con nuestro stack de desarrollo.

## 🐍 Backend - Python/FastAPI

### Extensiones Esenciales

1. **Python** (`ms-python.python`)
   - Soporte completo para Python
   - Incluye Pylance (IntelliSense avanzado)
   - Integración con debugpy para depuración

2. **Python Debugger** (`ms-python.debugpy`)
   - Depurador oficial de Python
   - Ya incluido con Python extension

3. **autoDocstring - Python Docstring Generator** (`njpwerner.autodocstring`)
   - Genera automáticamente docstrings para funciones
   - Soporta formatos Google, NumPy, Sphinx

4. **Error Lens** (`usernamehw.errorlens`)
   - Muestra errores y warnings inline en el código
   - Mejora significativamente la experiencia de desarrollo

### Extensiones de Productividad

5. **Black Formatter** (`ms-python.black-formatter`)
   - Formateo automático de código Python
   - Integrado con VS Code settings

6. **GitLens — Git supercharged** (`eamodio.gitlens`)
   - Potencia las capacidades Git de VS Code
   - Blame annotations, history, comparaciones

7. **Thunder Client** (`rangav.vscode-thunder-client`)
   - Cliente REST integrado en VS Code
   - Perfecto para probar APIs FastAPI

### Extensiones de Base de Datos

8. **SQLite Viewer** (`qwtel.sqlite-viewer`)
   - Visualizar bases de datos SQLite
   - Útil para desarrollo y debugging

9. **PostgreSQL** (`ckolkman.vscode-postgres`)
   - Cliente PostgreSQL integrado
   - Ejecutar consultas directamente desde VS Code

### Extensiones Docker

10. **Docker** (`ms-azuretools.vscode-docker`)
    - Manejo de contenedores y imágenes
    - Integración con Docker Compose
    - Logs de contenedores integrados

## ⚛️ Frontend - React/JavaScript/TypeScript

### Extensiones Esenciales

1. **ES7+ React/Redux/React-Native snippets** (`dsznajder.es7-react-js-snippets`)
   - Snippets esenciales para React
   - Incluye hooks, componentes, Redux patterns

2. **JavaScript and TypeScript Nightly** (`ms-vscode.vscode-typescript-next`)
   - Últimas características de TypeScript
   - Mejor IntelliSense para JavaScript/TypeScript

3. **Prettier - Code formatter** (`esbenp.prettier-vscode`)
   - Formateo automático de código
   - Soporta JavaScript, TypeScript, CSS, JSON, Markdown

### Extensiones de Productividad

4. **Auto Rename Tag** (`formulahendry.auto-rename-tag`)
   - Renombra automáticamente las etiquetas de cierre HTML/JSX
   - Esencial para desarrollo React

5. **Bracket Pair Colorizer 2** (`coenraads.bracket-pair-colorizer-2`)
   - Colorea los pares de brackets/paréntesis
   - **Nota**: VS Code 2021+ tiene esto integrado

6. **IntelliCode** (`visualstudioexptteam.vscodeintellicode`)
   - AI-assisted IntelliSense
   - Sugerencias inteligentes basadas en patrones

### Extensiones CSS/Styling

7. **CSS Peek** (`pranaygp.vscode-css-peek`)
   - Navegar rápidamente a definiciones CSS
   - Ver estilos sin cambiar de archivo

8. **Tailwind CSS IntelliSense** (`bradlc.vscode-tailwindcss`)
   - **Solo si usas Tailwind CSS**
   - Autocompletado para clases Tailwind

### Extensiones de Archivos

9. **vscode-icons** (`vscode-icons-team.vscode-icons`)
   - Iconos mejorados para tipos de archivo
   - Mejor navegación visual en el explorador

10. **Material Icon Theme** (`pkief.material-icon-theme`)
    - Alternativa a vscode-icons
    - Iconos estilo Material Design

## 🛠️ Extensiones Generales de Desarrollo

### Productividad General

1. **GitLens** (ya mencionado en Backend)
   - Útil para ambos frontend y backend

2. **Live Share** (`ms-vsliveshare.vsliveshare`)
   - Colaboración en tiempo real
   - Compartir sesiones de VS Code

3. **Todo Tree** (`gruntfuggly.todo-tree`)
   - Encuentra y resalta comentarios TODO, FIXME, etc.
   - Vista de árbol de tareas pendientes

4. **Better Comments** (`aaron-bond.better-comments`)
   - Mejora la visualización de comentarios
   - Diferentes colores para TODO, FIXME, etc.

### Temas y Apariencia

5. **One Dark Pro** (`zhuangtongfa.material-theme`)
   - Tema popular y fácil para los ojos
   - Buena legibilidad

6. **Material Theme** (`equinusocio.vscode-material-theme`)
   - Colección de temas Material Design
   - Múltiples variantes

## 📦 Instalación Rápida

### Método 1: Instalar individualmente
Copia y pega estos IDs en VS Code:
```
Ctrl+Shift+P → "Extensions: Install Extension" → Pegar ID
```

### Método 2: Via comando (Windows PowerShell)
```powershell
# Backend esenciales
code --install-extension ms-python.python
code --install-extension ms-python.debugpy
code --install-extension njpwerner.autodocstring
code --install-extension usernamehw.errorlens
code --install-extension ms-python.black-formatter
code --install-extension eamodio.gitlens
code --install-extension rangav.vscode-thunder-client
code --install-extension ms-azuretools.vscode-docker

# Frontend esenciales
code --install-extension dsznajder.es7-react-js-snippets
code --install-extension ms-vscode.vscode-typescript-next
code --install-extension esbenp.prettier-vscode
code --install-extension formulahendry.auto-rename-tag
code --install-extension visualstudioexptteam.vscodeintellicode
code --install-extension pranaygp.vscode-css-peek
code --install-extension vscode-icons-team.vscode-icons
```

## ⚙️ Configuración Recomendada

Después de instalar las extensiones, añade estas configuraciones en VS Code settings.json:

```json
{
    // Python
    "python.defaultInterpreterPath": "./.venv/Scripts/python.exe",
    "python.linting.enabled": true,
    "python.linting.flake8Enabled": true,
    "python.formatting.provider": "black",
    
    // JavaScript/TypeScript
    "typescript.preferences.importModuleSpecifier": "relative",
    "emmet.includeLanguages": {
        "javascript": "javascriptreact"
    },
    
    // Formateo automático
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
        "source.organizeImports": "explicit"
    },
    
    // Git
    "git.enableSmartCommit": true,
    "git.confirmSync": false
}
```

## 🎯 Prioridades de Instalación

### Instalación Mínima (Esencial)
1. Python extension
2. ES7+ React snippets  
3. Prettier
4. Error Lens
5. GitLens

### Instalación Completa (Recomendada)
- Todas las extensiones listadas arriba

### Instalación Avanzada (Opcional)
- Extensiones de temas
- Todo Tree
- Live Share
- Better Comments