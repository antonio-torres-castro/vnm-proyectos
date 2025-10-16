# 🚀 Flujo de Desarrollo para Windows

## 💻 Opciones de Terminal en Windows

Tu sistema Windows ofrece varias opciones para ejecutar comandos de desarrollo:

### 1. 🟦 **PowerShell (RECOMENDADO)**
- ✅ Mejor soporte para colores y funciones avanzadas
- ✅ Mejor manejo de errores
- ✅ Sintaxis más moderna
- **Archivo**: `comandos-desarrollo.ps1`

### 2. 🟨 **Command Prompt (CMD)**
- ✅ Disponible en todos los Windows
- ✅ Compatible con scripts batch tradicionales
- ⚠️ Limitaciones en funciones avanzadas
- **Archivo**: `comandos-desarrollo.bat`

### 3. 🐧 **WSL (Windows Subsystem for Linux)**
- ✅ Experiencia completa de Linux
- ✅ Uso del script original `.sh`
- ⚠️ Requiere instalación de WSL
- **Archivo**: `comandos-desarrollo.sh`

### 4. 🐙 **Git Bash**
- ✅ Incluye herramientas Linux
- ✅ Uso del script original `.sh`
- ⚠️ Puede tener limitaciones con Docker Desktop
- **Archivo**: `comandos-desarrollo.sh`

---

## 🎯 FLUJO RECOMENDADO PARA WINDOWS

### **Opción A: PowerShell (Mejor experiencia)**

#### Configuración Inicial (Una sola vez):
```powershell
# 1. Abrir PowerShell como Administrador
# 2. Permitir ejecución de scripts (si es necesario)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# 3. Navegar al directorio del proyecto
cd C:\ruta\a\tu\proyecto

# 4. Cargar funciones de desarrollo
. .\comandos-desarrollo.ps1
```

#### Uso Diario:
```powershell
# Verificar estado
Dev-Status

# Iniciar desarrollo
Dev-Start

# Ver logs
Dev-Logs

# Parar al final del día
Dev-Stop
```

### **Opción B: Command Prompt (CMD)**

#### Uso Directo:
```cmd
# Navegar al directorio del proyecto
cd C:\ruta\a\tu\proyecto

# Verificar estado
comandos-desarrollo.bat status

# Iniciar desarrollo
comandos-desarrollo.bat start

# Ver logs
comandos-desarrollo.bat logs

# Parar al final del día
comandos-desarrollo.bat stop
```

### **Opción C: Comandos Directos (Sin scripts)**

```cmd
# Para cualquier terminal (CMD, PowerShell, etc.)
python devtools/orquestador_desarrollo.py iniciar
python devtools/orquestador_desarrollo.py diagnosticar
python devtools/orquestador_desarrollo.py terminar
```

---

## 📋 COMANDOS PRINCIPALES POR PLATAFORMA

### 🟦 PowerShell

| Acción | Comando PowerShell | Descripción |
|--------|-------------------|-------------|
| **Ayuda** | `Show-DevHelp` | Ver todos los comandos |
| **Iniciar** | `Dev-Start` | Levantar entorno |
| **Estado** | `Dev-Status` | Verificar servicios |
| **Parar** | `Dev-Stop` | Parar con backup |
| **Limpiar** | `Dev-Stop-Clean` | Parar y limpiar |
| **Logs** | `Dev-Logs` | Ver logs |
| **Salud** | `Dev-Health` | Check de servicios |
| **Abrir** | `Dev-Open api` | Abrir en navegador |

### 🟨 Command Prompt (CMD)

| Acción | Comando CMD | Descripción |
|--------|-------------|-------------|
| **Ayuda** | `comandos-desarrollo.bat help` | Ver todos los comandos |
| **Iniciar** | `comandos-desarrollo.bat start` | Levantar entorno |
| **Estado** | `comandos-desarrollo.bat status` | Verificar servicios |
| **Parar** | `comandos-desarrollo.bat stop` | Parar con backup |
| **Limpiar** | `comandos-desarrollo.bat stop-clean` | Parar y limpiar |
| **Logs** | `comandos-desarrollo.bat logs` | Ver logs |
| **Salud** | `comandos-desarrollo.bat health` | Check de servicios |
| **Abrir** | `comandos-desarrollo.bat open api` | Abrir en navegador |

### 🐧 WSL/Git Bash (Linux-style)

| Acción | Comando Bash | Descripción |
|--------|--------------|-------------|
| **Cargar** | `source comandos-desarrollo.sh` | Cargar funciones |
| **Ayuda** | `dev-help` | Ver todos los comandos |
| **Iniciar** | `dev-start` | Levantar entorno |
| **Estado** | `dev-status` | Verificar servicios |
| **Parar** | `dev-stop` | Parar con backup |
| **Limpiar** | `dev-stop-clean` | Parar y limpiar |

---

## 🔧 CONFIGURACIÓN ESPECÍFICA PARA WINDOWS

### 📂 Estructura de Archivos para Windows

```
tu-proyecto/
├── 📁 .vscode/                          # Configuración VS Code
│   ├── 📄 launch.json                   # Depuración
│   ├── 📄 tasks.json                    # Tareas automatizadas
│   └── 📄 settings.json                 # Configuración
├── 📄 comandos-desarrollo.ps1           # ✅ PowerShell (Windows)
├── 📄 comandos-desarrollo.bat           # ✅ CMD (Windows)
├── 📄 comandos-desarrollo.sh            # Linux/WSL/Git Bash
└── 📁 devtools/
    └── 📄 orquestador_desarrollo.py     # Script principal
```

### 🐳 Docker Desktop para Windows

Asegúrate de que Docker Desktop esté:
- ✅ Instalado y ejecutándose
- ✅ Con WSL 2 habilitado (recomendado)
- ✅ Con acceso desde PowerShell/CMD

```powershell
# Verificar Docker
docker --version
docker-compose --version
```

### 🔑 Permisos de PowerShell

Si recibes error de "execution policy":

```powershell
# Como Administrador (una sola vez)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# O para el proyecto específico
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process
```

---

## 🎯 FLUJOS DE TRABAJO WINDOWS

### 📅 **Inicio de Día - PowerShell**

```powershell
# 1. Abrir PowerShell en el directorio del proyecto
cd C:\tu-proyecto

# 2. Cargar comandos de desarrollo
. .\comandos-desarrollo.ps1

# 3. Verificar estado
Dev-Status

# 4. Iniciar si es necesario
Dev-Start

# 5. Para VS Code: Presionar F5 → "FullStack Debug"
```

### 📅 **Inicio de Día - CMD**

```cmd
# 1. Abrir CMD en el directorio del proyecto
cd C:\tu-proyecto

# 2. Verificar estado
comandos-desarrollo.bat status

# 3. Iniciar si es necesario
comandos-desarrollo.bat start
```

### 🔍 **Monitoreo - PowerShell**

```powershell
# Ver estado general
Dev-Status

# Verificar salud de servicios
Dev-Health

# Ver logs en tiempo real
Dev-Logs

# Ver contenedores activos
Dev-PS
```

### 🔍 **Monitoreo - CMD**

```cmd
# Ver estado general
comandos-desarrollo.bat status

# Verificar salud de servicios
comandos-desarrollo.bat health

# Ver logs en tiempo real
comandos-desarrollo.bat logs
```

### 🌐 **Abrir URLs - PowerShell**

```powershell
# Abrir en navegador directamente
Dev-Open api         # http://localhost:8000
Dev-Open docs        # http://localhost:8000/docs
Dev-Open frontend    # http://localhost:3000
Dev-Open pgadmin     # http://localhost:5050
```

### 🌐 **Abrir URLs - CMD**

```cmd
# Abrir en navegador directamente
comandos-desarrollo.bat open api
comandos-desarrollo.bat open docs
comandos-desarrollo.bat open frontend
comandos-desarrollo.bat open pgadmin
```

### 🏁 **Fin de Día**

```powershell
# PowerShell
Dev-Stop

# CMD
comandos-desarrollo.bat stop

# Directo
python devtools/orquestador_desarrollo.py terminar
```

---

## 🚀 DEPURACIÓN EN VS CODE (WINDOWS)

### Configuración VS Code para Windows

```json
// .vscode/settings.json (ya configurado)
{
    "python.defaultInterpreterPath": "./.venv/Scripts/python.exe",
    "terminal.integrated.defaultProfile.windows": "PowerShell",
    "terminal.integrated.profiles.windows": {
        "PowerShell": {
            "source": "PowerShell",
            "args": ["-NoExit", "-File", "${workspaceFolder}/comandos-desarrollo.ps1"]
        }
    }
}
```

### Flujo de Depuración

1. **Abrir VS Code** en el directorio del proyecto
2. **Presionar F5**
3. **Seleccionar "FullStack Debug"**
4. VS Code ejecutará automáticamente:
   - Inicio del orquestador
   - Backend FastAPI con depuración
   - Frontend React con depuración
   - Apertura del navegador

---

## 🛠️ TROUBLESHOOTING WINDOWS

### Error: "Docker no encontrado"
```powershell
# Verificar instalación
docker --version

# Si no está instalado:
# 1. Descargar Docker Desktop desde docker.com
# 2. Instalar y reiniciar
# 3. Habilitar WSL 2 si se solicita
```

### Error: "Python no encontrado"
```powershell
# Verificar instalación
python --version

# Si no está instalado:
# 1. Descargar Python desde python.org
# 2. Marcar "Add to PATH" durante instalación
# 3. Reiniciar terminal
```

### Error: "Execution Policy"
```powershell
# Ejecutar como Administrador
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Error: "Puerto en uso"
```powershell
# Ver qué usa el puerto
netstat -ano | findstr :8000

# Parar servicios
Dev-Stop
# O: comandos-desarrollo.bat stop
```

### Error: "Volúmenes llenos"
```powershell
# Limpiar Docker
Dev-Clean-Docker
# O: comandos-desarrollo.bat clean-docker
```

---

## 🎯 COMPARACIÓN DE OPCIONES

| Característica | PowerShell | CMD | WSL/Git Bash |
|----------------|------------|-----|--------------|
| **Colores** | ✅ Excelente | ⚠️ Básico | ✅ Excelente |
| **Funciones** | ✅ Avanzado | ⚠️ Básico | ✅ Completo |
| **Autocompletado** | ✅ Sí | ❌ No | ✅ Sí |
| **Disponibilidad** | ✅ Windows 7+ | ✅ Todos | ⚠️ Requiere instalación |
| **Docker Integration** | ✅ Nativo | ✅ Nativo | ⚠️ Puede requerir config |
| **Recomendación** | 🥇 **MEJOR** | 🥉 Básico | 🥈 Avanzado |

---

## 📋 RESUMEN EJECUTIVO WINDOWS

### 🟦 **PowerShell (RECOMENDADO)**
```powershell
# Configuración inicial
. .\comandos-desarrollo.ps1

# Flujo diario
Dev-Status    # Verificar
Dev-Start     # Iniciar
# Desarrollar...
Dev-Stop      # Terminar
```

### 🟨 **Command Prompt**
```cmd
# Flujo diario
comandos-desarrollo.bat status    # Verificar
comandos-desarrollo.bat start     # Iniciar
# Desarrollar...
comandos-desarrollo.bat stop      # Terminar
```

### 🎯 **Comandos Directos (Universal)**
```cmd
python devtools/orquestador_desarrollo.py diagnosticar
python devtools/orquestador_desarrollo.py iniciar
python devtools/orquestador_desarrollo.py terminar
```

---

## 🎉 ¡LISTO PARA DESARROLLAR EN WINDOWS!

**Elige tu opción preferida:**
- **Principiante**: CMD con `comandos-desarrollo.bat`
- **Avanzado**: PowerShell con `comandos-desarrollo.ps1`
- **Purista Linux**: WSL con `comandos-desarrollo.sh`

**Tu flujo diario será**:
1. 🔍 Verificar estado
2. 🚀 Iniciar entorno
3. 🎨 Desarrollar (con VS Code F5)
4. 🛑 Parar al final

---

**Configurado por**: MiniMax Agent  
**Fecha**: 2025-10-14  
**Plataforma**: Windows con Docker Desktop  
**Estado**: ✅ **COMPLETAMENTE FUNCIONAL**
