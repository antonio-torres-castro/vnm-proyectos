# 🎯 RESUMEN FINAL: Flujo de Desarrollo VNM-Proyectos

## 🚀 COMANDOS RÁPIDOS DE UN VISTAZO

### 💻 WINDOWS (Tu Plataforma)

#### 🟦 PowerShell (RECOMENDADO)
```powershell
# 1. Cargar comandos rápidos
. .\comandos-desarrollo.ps1

# 2. Ver ayuda
Show-DevHelp

# 3. Comandos principales
Dev-Start         # Iniciar desarrollo
Dev-Status        # Verificar estado  
Dev-Stop          # Parar (con backup)
Dev-Stop-Clean    # Parar y limpiar todo
```

#### 🟨 Command Prompt (CMD)
```cmd
# Comandos directos (sin cargar)
comandos-desarrollo.bat help     # Ver ayuda
comandos-desarrollo.bat start    # Iniciar desarrollo
comandos-desarrollo.bat status   # Verificar estado
comandos-desarrollo.bat stop     # Parar (con backup)
comandos-desarrollo.bat stop-clean  # Parar y limpiar todo
```

### 🐧 Linux/WSL/Git Bash
```bash
# 1. Cargar comandos rápidos
source comandos-desarrollo.sh

# 2. Ver ayuda
dev-help

# 3. Comandos principales
dev-start         # Iniciar desarrollo
dev-status        # Verificar estado  
dev-stop          # Parar (con backup)
dev-stop-clean    # Parar y limpiar todo
```

### 🔧 Comandos Directos del Orquestador
```bash
# Básicos
python devtools/orquestador_desarrollo.py iniciar
python devtools/orquestador_desarrollo.py diagnosticar
python devtools/orquestador_desarrollo.py terminar
python devtools/orquestador_desarrollo.py terminar --limpiar-completo

# Avanzados
python devtools/orquestador_desarrollo.py iniciar --rebuild
python devtools/orquestador_desarrollo.py regenerar
python devtools/orquestador_desarrollo.py backup
```

---

## 🔄 FLUJOS DE TRABAJO ESENCIALES

### 📅 1. INICIO DE DÍA
```bash
# Opción A: Comandos rápidos
source comandos-desarrollo.sh
dev-status    # Verificar estado
dev-start     # Iniciar si es necesario

# Opción B: Comandos directos
python devtools/orquestador_desarrollo.py diagnosticar
python devtools/orquestador_desarrollo.py iniciar
```

### 🔍 2. DEPURACIÓN EN VS CODE
```bash
# 1. En VS Code: Presiona F5
# 2. Selecciona "FullStack Debug"
# 3. ¡Automático! VS Code ejecuta todo
```

### 🛠️ 3. CAMBIOS EN DOCKER/DEPENDENCIAS
```bash
# Cuando cambias Dockerfile, requirements.txt, package.json
dev-start-rebuild
# O: python devtools/orquestador_desarrollo.py iniciar --rebuild
```

### 🔧 4. SOLUCIONAR PROBLEMAS
```bash
# Diagnóstico detallado
python devtools/orquestador_desarrollo.py diagnosticar --verboso

# Ver logs
dev-logs          # Todos los servicios
dev-logs-backend  # Solo backend
dev-logs-db       # Solo PostgreSQL

# Regenerar si hay problemas graves
dev-restart
# O: python devtools/orquestador_desarrollo.py regenerar
```

### 🏁 5. FIN DE DÍA
```bash
# Opción A: Parar con backup (recomendado)
dev-stop
# O: python devtools/orquestador_desarrollo.py terminar

# Opción B: Dejar corriendo para mañana
# (No hacer nada)
```

### 🧹 6. LIMPIEZA COMPLETA
```bash
# Cuando necesites empezar completamente limpio
dev-stop-clean
# O: python devtools/orquestador_desarrollo.py terminar --limpiar-completo
```

---

## 🎛️ OPCIONES AVANZADAS

### 🐘 Con PgAdmin (Administración de BD)
```bash
# Iniciar con PgAdmin incluido
dev-start-pgadmin
# O: docker-compose -f docker-compose.debug.yml --profile pgadmin up -d

# Acceder: http://localhost:5050
# Usuario: admin@monitoreo.dev
# Contraseña: admin123
```

### 💾 Backups
```bash
# Backup manual (sin parar servicios)
dev-backup
# O: python devtools/orquestador_desarrollo.py backup

# Los backups se guardan en .backups/
```

### 🔍 Monitoreo Continuo
```bash
# Estado de contenedores
dev-ps
# O: docker ps

# Salud de servicios
dev-health

# Logs en tiempo real
dev-logs
# O: docker-compose -f docker-compose.debug.yml logs -f
```

---

## 🌐 URLs IMPORTANTES

| Servicio | URL | Descripción |
|----------|-----|-------------|
| **Backend API** | http://localhost:8000 | API FastAPI |
| **API Docs** | http://localhost:8000/docs | Documentación interactiva |
| **Health Check** | http://localhost:8000/health | Verificación de salud |
| **Frontend** | http://localhost:3000 | Aplicación React |
| **PgAdmin** | http://localhost:5050 | Admin de PostgreSQL (opcional) |

---

## 📊 ESTADOS DEL ENTORNO

### ✅ ENTORNO SALUDABLE
```
✓ PostgreSQL: running (puerto 5432)
✓ Redis: running (puerto 6379) 
✓ Backend API: healthy (puerto 8000)
✓ Frontend: running (puerto 3000)
🎉 ENTORNO COMPLETAMENTE OPERATIVO
```

### ⚠️ ENTORNO PROBLEMÁTICO
```
✗ PostgreSQL: stopped
✓ Redis: running
⚠ Backend API: no response
✗ Frontend: not running
❌ ENTORNO PARCIALMENTE OPERATIVO
```

**Solución**: `dev-restart` o `python devtools/orquestador_desarrollo.py regenerar`

---

## 🛠️ TROUBLESHOOTING RÁPIDO

### Problema: "Docker no está ejecutándose"
```bash
# Linux/macOS
sudo systemctl start docker

# Windows
# Iniciar Docker Desktop
```

### Problema: "Puerto ya en uso"
```bash
# Parar contenedores existentes
dev-stop
# O: docker-compose -f docker-compose.debug.yml down
```

### Problema: "Base de datos corrupta"
```bash
# Regenerar entorno completo
dev-restart
```

### Problema: "Volúmenes llenos"
```bash
# Limpiar recursos no utilizados
dev-clean-docker
# O: docker system prune -f && docker volume prune -f
```

### Problema: "Frontend no carga"
```bash
# Ver logs del frontend
dev-logs-backend

# Verificar dependencias
cd frontend && npm install
```

---

## 🎯 CONFIGURACIÓN INICIAL (UNA SOLA VEZ)

### 💻 Windows

#### PowerShell
```powershell
# 1. Permitir ejecución de scripts (como Administrador)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# 2. Crear perfil permanente (opcional)
New-Item -Path $PROFILE -Type File -Force
Add-Content -Path $PROFILE -Value ". $(Get-Location)\comandos-desarrollo.ps1"
```

#### Command Prompt
```cmd
# No requiere configuración especial
# Usar directamente: comandos-desarrollo.bat [comando]
```

### 🐧 Linux/WSL/Git Bash

```bash
# Agregar al perfil de shell (~/.bashrc, ~/.zshrc, etc.)
echo "source $(pwd)/comandos-desarrollo.sh" >> ~/.bashrc
# O para zsh:
echo "source $(pwd)/comandos-desarrollo.sh" >> ~/.zshrc

# Recargar shell
source ~/.bashrc  # o ~/.zshrc
```

### 2. Verificar Configuración
```bash
# Verificar que VS Code está configurado
ls -la .vscode/
# Deberías ver: extensions.json, launch.json, settings.json, tasks.json

# Verificar orquestador
python devtools/orquestador_desarrollo.py --help
```

### 3. Primera Ejecución
```bash
# Iniciar por primera vez
dev-start
# O: python devtools/orquestador_desarrollo.py iniciar

# Verificar que todo funciona
dev-status
dev-health
```

---

## 📚 ARCHIVOS DE DOCUMENTACIÓN

| Archivo | Propósito | Plataforma |
|---------|-----------|------------|
| <filepath>FLUJO_DESARROLLO_COMPLETO.md</filepath> | Guía detallada completa | Universal |
| <filepath>FLUJO_DESARROLLO_WINDOWS.md</filepath> | **Guía específica para Windows** | **Windows** |
| <filepath>comandos-desarrollo.ps1</filepath> | **Script PowerShell** | **Windows** |
| <filepath>comandos-desarrollo.bat</filepath> | **Script Command Prompt** | **Windows** |
| <filepath>comandos-desarrollo.sh</filepath> | Script Bash | Linux/WSL/Git Bash |
| <filepath>CONFIGURACION_DEPURACION_VSCODE.md</filepath> | Guía de depuración VS Code | Universal |
| <filepath>DEPURACION_CONFIGURADA.md</filepath> | Resumen de configuración VS Code | Universal |
| <filepath>PGLADMIN_CONFIGURACION.md</filepath> | Configuración de PgAdmin | Universal |

---

## 🎯 DECISIONES PARA DIFERENTES ESCENARIOS

### 🔹 Desarrollo Diario Normal
**Usar**: `dev-start` → desarrollar → `dev-stop`

### 🔹 Depuración Full-Stack
**Usar**: VS Code F5 → "FullStack Debug"

### 🔹 Cambios en Docker
**Usar**: `dev-start-rebuild`

### 🔹 Problemas del Entorno
**Usar**: `dev-restart`

### 🔹 Administrar Base de Datos
**Usar**: `dev-start-pgadmin` → http://localhost:5050

### 🔹 Liberar Espacio en Disco
**Usar**: `dev-stop-clean`

### 🔹 Backup Antes de Cambios Importantes
**Usar**: `dev-backup`

---

## ✅ CHECKLIST DE VERIFICACIÓN

### ☑️ Antes de Empezar
- [ ] Docker está instalado y ejecutándose
- [ ] VS Code está instalado (opcional, para depuración)
- [ ] El proyecto está clonado completamente
- [ ] Estás en el directorio raíz del proyecto

### ☑️ Configuración Inicial
- [ ] Comandos rápidos cargados: `source comandos-desarrollo.sh`
- [ ] Primer inicio exitoso: `dev-start`
- [ ] Diagnóstico saludable: `dev-status`
- [ ] URLs accesibles: http://localhost:8000 y http://localhost:3000

### ☑️ VS Code (Opcional)
- [ ] Extensiones recomendadas instaladas
- [ ] F5 → "FullStack Debug" funciona
- [ ] Breakpoints funcionan en Python y TypeScript

---

## 🚀 ¡LISTO PARA DESARROLLAR!

**Tu flujo diario será tan simple como**:
1. `dev-start` (o F5 en VS Code)
2. **Desarrollar** 🎨
3. `dev-stop` (al final del día)

**¿Problemas?** → `dev-restart`  
**¿Dudas?** → `dev-help`

---

**Configurado por**: MiniMax Agent  
**Fecha**: 2025-10-14  
**Estado**: ✅ **COMPLETAMENTE FUNCIONAL**
