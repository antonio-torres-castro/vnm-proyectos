# 🚀 VNM-Proyectos - Sistema de Monitoreo de Red

**Proyecto completo de monitoreo de dispositivos de red con interfaz web moderna y API robusta**

## 📁 Estructura del Proyecto

```
vnm-proyectos/
├── 📄 README.md                    # Este archivo
├── 📄 vnm_automate.py             # Script maestro de automatización ⭐
├── 📄 setup_proyecto.py           # Configuración inicial del proyecto
├── 📄 inicio_rapido.bat          # Script inicio rápido Windows
├── 📄 inicio_rapido.ps1          # Script inicio rápido PowerShell
├── 📄 .vscode/                   # Configuración VS Code para la solución completa
│
├── 📁 backend/                    # API FastAPI + Base de datos
│   ├── 📁 app/                   # Código de la aplicación
│   ├── 📁 .vscode/              # Configuración VS Code específica backend
│   └── 📄 requirements.txt      # Dependencias Python
│
├── 📁 frontend/                   # Interfaz React + Vite
│   ├── 📁 src/                   # Código fuente React
│   ├── 📁 .vscode/              # Configuración VS Code específica frontend  
│   └── 📄 package.json          # Dependencias Node.js
│
├── 📁 database/                   # Configuración PostgreSQL + pgAdmin
│   ├── 📁 backups/              # Backups automáticos
│   ├── 📁 scripts/              # Scripts SQL
│   └── 📄 init.sql              # Inicialización de DB
│
├── 📁 automate/                   # 🤖 Todos los automatismos
│   ├── 📁 devtools/             # Herramientas de desarrollo
│   ├── 📄 instalar_vscode_config.py    # Instalador VS Code
│   ├── 📄 verificar_vscode_instalado.py # Verificador VS Code
│   ├── 📄 formatear_codigo.py          # Formateador código
│   └── 📄 ...otros automatismos
│
├── 📁 vscode-config/             # Plantillas configuración VS Code
│   ├── 📄 launch.json           # Configuraciones debugging
│   ├── 📄 tasks.json            # Tareas automatizadas
│   ├── 📄 settings.json         # Configuración workspace
│   └── 📄 extensions.json       # Extensiones recomendadas
│
├── 📁 info/                      # 📚 Toda la documentación
│   ├── 📄 README_INSTALACION_VSCODE.md
│   ├── 📄 FLUJO_DESARROLLO_WINDOWS.md
│   ├── 📄 CONFIGURACION_DEBUG_VSCODE_CORREGIDA.md
│   └── 📄 ...más documentación
│
├── 📁 logs/                      # Logs del sistema
└── 📁 mislogs/                   # Logs personalizados
```

## 🚀 Inicio Rápido

### 1. **Configuración Inicial (Solo la primera vez)**
```bash
cd vnm-proyectos
python setup_proyecto.py
```

### 2. **Iniciar Desarrollo**
```bash
# Método 1: Script maestro (recomendado)
python vnm_automate.py dev-start

# Método 2: Windows (doble clic)
inicio_rapido.bat
```

### 3. **Debugging en VS Code**
1. Abrir VS Code: `code .`
2. Instalar extensiones recomendadas
3. Presionar **F5**
4. Seleccionar: **"FullStack Debug - Ambos simultáneamente"**

## 🎯 Script Maestro - vnm_automate.py

**Centraliza todos los automatismos en un solo comando desde el directorio raíz.**

### Comandos de Desarrollo
```bash
python vnm_automate.py dev-start      # Iniciar entorno completo
python vnm_automate.py dev-stop       # Detener entorno
python vnm_automate.py dev-status     # Diagnóstico del entorno
python vnm_automate.py dev-restart    # Reiniciar entorno completo
python vnm_automate.py dev-backup     # Backup de base de datos
```

### Comandos de VS Code
```bash
python vnm_automate.py vscode-install # Instalar configuración VS Code
python vnm_automate.py vscode-verify  # Verificar configuración VS Code
```

### Comandos de Código
```bash
python vnm_automate.py code-format    # Formatear código (Black + Flake8)
python vnm_automate.py code-validate  # Validar código sin formatear
```

### Comandos de Base de Datos
```bash
python vnm_automate.py db-recreate    # Recrear DB desde cero
python vnm_automate.py db-backup      # Backup manual
```

### Comandos de Testing
```bash
python vnm_automate.py test-all       # Ejecutar todos los tests
python vnm_automate.py test-backend   # Tests del backend
python vnm_automate.py test-frontend  # Tests del frontend
```

### Ver Todos los Comandos
```bash
python vnm_automate.py help
```

## 🔧 Configuraciones VS Code

### Solución Completa (vnm-proyectos/.vscode/)
- **FullStack Debug - Ambos simultáneamente** ⭐ (Recomendado)
- **FullStack Debug - Compound** (Alternativo)
- **Frontend Debug** (Solo React)
- **Backend Debug** (Solo FastAPI)

### Proyectos Individuales
- **backend/.vscode/** - Configuración específica para backend
- **frontend/.vscode/** - Configuración específica para frontend

## 📋 Requisitos del Sistema

### Obligatorios
- **Python 3.7+**
- **Docker Desktop** (ejecutándose)
- **Node.js y npm**
- **VS Code** (recomendado)

### Puertos Necesarios
- **3000** - Frontend React
- **8000** - Backend FastAPI
- **5432** - PostgreSQL
- **8080** - pgAdmin

### Sistema Operativo
- **Windows** ✅ (optimizado)
- **Linux/macOS** ✅ (compatible)

## 🛠️ Flujo de Desarrollo

### Desarrollo Normal
1. `python vnm_automate.py dev-start` - Iniciar entorno
2. `code .` - Abrir VS Code
3. **F5** → "FullStack Debug - Ambos simultáneamente" 
4. Desarrollar con debugging completo
5. `python vnm_automate.py dev-stop` - Detener cuando termines

### Desarrollo Backend Solo
```bash
cd backend
code .  # VS Code con configuración específica backend
```

### Desarrollo Frontend Solo
```bash
cd frontend
code .  # VS Code con configuración específica frontend
```

## 📚 Documentación Detallada

Toda la documentación detallada está en la carpeta <filepath>info/</filepath>:

- **Instalación VS Code**: `info/README_INSTALACION_VSCODE.md`
- **Desarrollo Windows**: `info/FLUJO_DESARROLLO_WINDOWS.md`
- **Configuración Debug**: `info/CONFIGURACION_DEBUG_VSCODE_CORREGIDA.md`
- **Y mucho más...**

## 🔄 Automatismos Disponibles

Todos los automatismos están en <filepath>automate/</filepath>:

### Herramientas de Desarrollo (automate/devtools/)
- **orquestador_desarrollo.py** - Gestión completa del entorno Docker
- **validar_orquestador.py** - Validación del orquestador

### Automatismos de VS Code (automate/)
- **instalar_vscode_config.py** - Instalador configuración VS Code
- **verificar_vscode_instalado.py** - Verificador configuración

### Automatismos de Código (automate/)
- **formatear_codigo.py** - Formateador con Black y Flake8
- **diagnosticar_backend.py** - Diagnóstico del backend

### Automatismos de Base de Datos (automate/)
- **recrear_base_datos.py** - Recreador de base de datos

## ✅ Ventajas de la Nueva Estructura

### 🎯 **Centralización**
- Un solo comando para todo: `vnm_automate.py`
- No más navegación entre carpetas

### 📁 **Organización**
- Automatismos separados de código fuente
- Documentación centralizada en `info/`
- Configuraciones específicas por proyecto

### 🐞 **Debugging Mejorado**
- Configuración VS Code corregida (sin errores)
- Debug FullStack funcional
- Configuraciones específicas por componente

### 🖥️ **Optimizado para Windows**
- Scripts .bat y .ps1 incluidos
- Detección automática de sistema operativo
- Configuraciones específicas Windows

### 🔄 **Mantenibilidad**
- Automatismos versionados y organizados
- Fácil actualización y mantenimiento
- Scripts de verificación incluidos

## 🆘 Solución de Problemas

### ❌ Error "Attribute 'request' is missing"
**SOLUCIONADO** ✅ - La nueva configuración VS Code elimina este error completamente.

### 🐳 Docker no arranca
```bash
python vnm_automate.py dev-status  # Diagnosticar problema
```

### 🔧 VS Code no reconoce configuración
```bash
python vnm_automate.py vscode-verify  # Verificar instalación
python vnm_automate.py vscode-install # Reinstalar si es necesario
```

### 📝 Problemas de formato código
```bash
python vnm_automate.py code-format    # Formatear automáticamente
```

## 🏆 Estado del Proyecto

- ✅ **Estructura reorganizada y optimizada**
- ✅ **Debugging VS Code completamente funcional**
- ✅ **Automatismos centralizados y mejorados** 
- ✅ **Documentación actualizada y organizada**
- ✅ **Scripts específicos para Windows**
- ✅ **Configuraciones VS Code por proyecto**
- ✅ **Script maestro de automatización**

---

**📅 Última actualización**: 2025-10-14 21:02:38  
**👨‍💻 Autor**: MiniMax Agent  
**🏷️ Versión**: 2.0 - Estructura Reorganizada
