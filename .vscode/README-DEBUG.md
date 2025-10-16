# Debug Guide for VS Code

Simple guide for the 3 debugging configurations available.

## Prerequisites

**Always run first:** `python automate\inicio_desarrollo.py`
This script prepares the Docker development environment:
- Installs frontend dependencies (npm install)
- Starts Docker containers
- Verifies service readiness

**VS Code Setup:** See <filepath>_vscode/EXTENSIONES-RECOMENDADAS.md</filepath> for recommended extensions.

## Available Configurations

### 1. Frontend Debug
- **Context:** Open VS Code in `vnm-proyectos\frontend\` folder
- **Usage:** Debug only React frontend
- **Steps:**
  1. Run `python automate\inicio_desarrollo.py` from root
  2. Open VS Code in `frontend` folder: `cd frontend && code .`
  3. Press F5

### 2. Backend Debug  
- **Context:** Open VS Code in `vnm-proyectos\backend\` folder
- **Usage:** Debug only Python backend
- **Steps:**
  1. Run `python automate\inicio_desarrollo.py` from root
  2. Open VS Code in `backend` folder: `cd backend && code .`
  3. Press F5

### 3. FullStack Debug
- **Context:** Open VS Code in `vnm-proyectos\` root folder
- **Usage:** Debug both frontend and backend simultaneously
- **Steps:**
  1. Run `python automate\inicio_desarrollo.py`
  2. Open VS Code in root folder: `code .`
  3. Press F5

## Services After inicio_desarrollo.py

When the script completes successfully, you will have:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000 (after F5)
- PostgreSQL: localhost:5432
- Debug Server: localhost:5678

## Data Management

**Important:** Data is preserved by default in all operations.

### Closing Environment
- **Preserve data:** `python automate\cerrar_desarrollo.py`
- **Quick stop:** `python automate\cerrar_desarrollo.py --simple`
- **Delete all data:** `python automate\cerrar_desarrollo.py --complete`

### Data Storage
Database data is stored in Docker volumes that persist between restarts.
Only the `--complete` option will delete your data.

## Troubleshooting

### Services not starting
**Solution:** Run `python automate\inicio_desarrollo.py` again

### Breakpoints not working
**Solution:** 
1. Verify you opened VS Code in the correct folder context
2. Verify services are running with the startup script

### Backend not responding
**Solution:** 
1. Check if `inicio_desarrollo.py` completed successfully
2. Verify with: `docker ps`

### Data lost accidentally
**Solution:** 
1. Check if you used `--complete` option when closing
2. Database data only survives if you used normal closure

## Notes

- Use the centralized automation in `automate\` folder
- Each configuration works in its specific folder context
- The startup script handles all service preparation automatically

## VS Code Setup Guide

### Required Extensions

For optimal development experience, install the recommended VS Code extensions:

**See complete guide:** <filepath>_vscode/EXTENSIONES-RECOMENDADAS.md</filepath>

**Quick install (essential):**
```bash
# Backend essentials
code --install-extension ms-python.python
code --install-extension usernamehw.errorlens
code --install-extension eamodio.gitlens
code --install-extension ms-azuretools.vscode-docker

# Frontend essentials  
code --install-extension dsznajder.es7-react-js-snippets
code --install-extension esbenp.prettier-vscode
code --install-extension formulahendry.auto-rename-tag
```

### Python Import Errors

If you see Pylance errors like:
```
Import "sqlalchemy" could not be resolved
```

**Manual Solution:**
```bash
# Option 1: Complete setup (may fail on Windows due to native dependencies)
python automate/configurar_entorno_local.py

# Option 2: Windows-specific setup (recommended)
python automate/configurar_entorno_windows.py

# Option 3: Quick fix with fallback
python automate/fix_vscode_imports.py
```

**After setup:**
1. Restart VS Code
2. Import errors should disappear
3. Code analysis and IntelliSense will work properly

**Important:** These local environments are only for VS Code analysis. Actual execution happens in Docker containers.
