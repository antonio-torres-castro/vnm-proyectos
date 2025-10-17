# 🚀 VNM-Proyectos - Sistema de Monitoreo de Red

**Proyecto completo de monitoreo de dispositivos de red con interfaz web moderna y API robusta**

## 📁 Estructura del Proyecto

```
vnm-proyectos/
├── 📄 README.md                    # Este archivo
├── 📁 automate/                    # 🔧 Scripts de automatización
│   ├── 📄 inicio_desarrollo.py    # Iniciar entorno completo
│   ├── 📄 cerrar_desarrollo.py    # Cerrar entorno
│   ├── 📄 instalar_extensiones_vscode.py  # Instalar extensiones VS Code
│   ├── 📄 configurar_entorno_windows.py   # Configurar Python local
│   ├── 📄 utilidades.py           # Menú interactivo de herramientas
│   └── 📄 verificar_configuracion_completa.py # Diagnóstico
├── 📁 _vscode/                     # Configuración VS Code
│   ├── 📄 README-DEBUG.md         # Guía de debugging
│   ├── 📄 EXTENSIONES-RECOMENDADAS.md # Lista de extensiones
│   ├── 📄 settings.json           # Configuración del editor
│   └── 📄 launch.json             # Configuraciones de debug
│
├── 📁 backend/                     # API FastAPI + Base de datos
│   ├── 📁 app/                    # Código de la aplicación
│   ├── 📄 requirements.txt       # Dependencias Python completas
│   ├── 📄 requirements-dev.txt   # Dependencias para VS Code (Windows)
│   └── 📄 Dockerfile.dev          # Container de desarrollo
│
├── 📁 frontend/                    # Interfaz React + Vite
│   ├── 📁 src/                    # Código fuente React
│   ├── 📄 package.json           # Dependencias Node.js
│   └── 📄 Dockerfile.dev          # Container de desarrollo
│
├── 📁 database/                    # Configuración PostgreSQL
│   ├── 📁 scripts/               # Scripts SQL de inicialización
│   └── 📄 init.sql               # Esquema inicial
│
└── 📄 docker-compose.debug.yml    # Orquestación de servicios
```
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

### 1. **Iniciar Desarrollo**
```bash
# Desde vnm-proyectos/
python automate/inicio_desarrollo.py
```
Este comando:
- Instala dependencias del frontend (npm install)
- Inicia todos los servicios Docker
- Prepara el entorno completo

### 2. **Configurar VS Code (primera vez)**
```bash
# Instalar extensiones recomendadas
python automate/instalar_extensiones_vscode.py

# Configurar entorno Python local (para evitar errores de importación)
python automate/configurar_entorno_windows.py
```

### 3. **Debugging en VS Code**
1. Abrir VS Code: `code .`
2. Presionar **F5**
3. Seleccionar: **"Backend: FastAPI Docker Debug"**
4. ¡Listo! La aplicación está corriendo

### 4. **Servicios Disponibles**
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000 (después de F5)
- **PostgreSQL**: localhost:5432

### 5. **Cerrar Entorno**
```bash
# Cerrar manteniendo datos
python automate/cerrar_desarrollo.py

# Cerrar rápido (solo parar)
python automate/cerrar_desarrollo.py --simple
```

## 🛠️ Herramientas de Desarrollo

### Script de Utilidades
```bash
# Acceso a todas las herramientas en un menú interactivo
python automate/utilidades.py
```

### Scripts Individuales
```bash
# Gestión del entorno
python automate/inicio_desarrollo.py          # Iniciar desarrollo
python automate/cerrar_desarrollo.py          # Cerrar (mantener datos)
python automate/verificar_configuracion_completa.py  # Diagnóstico

# Configuración VS Code
python automate/instalar_extensiones_vscode.py    # Instalar extensiones
python automate/configurar_entorno_windows.py     # Configurar Python local
python automate/fix_vscode_imports.py             # Solucionar errores importación
```

### Comandos de Base de Datos
```bash
python automate/vnm_automate.py db-recreate    # Recrear DB desde cero
python automate/vnm_automate.py db-backup      # Backup manual
```

### Comandos de Testing
```bash
python automate/vnm_automate.py test-all       # Ejecutar todos los tests
python automate/vnm_automate.py test-backend   # Tests del backend
python automate/vnm_automate.py test-frontend  # Tests del frontend
```

### Ver Todos los Comandos
```bash
python automate/vnm_automate.py help
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
1. `python automate/vnm_automate.py dev-start` - Iniciar entorno
2. `code .` - Abrir VS Code
3. **F5** → "FullStack Debug - Ambos simultáneamente" 
4. Desarrollar con debugging completo
5. `python automate/vnm_automate.py dev-stop` - Detener cuando termines

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
- Un solo comando para todo: `automate/vnm_automate.py`
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
python automate/vnm_automate.py dev-status  # Diagnosticar problema
```

### 🔧 VS Code no reconoce configuración
```bash
python automate/vnm_automate.py vscode-verify  # Verificar instalación
python automate/vnm_automate.py vscode-install # Reinstalar si es necesario
```

### 📝 Problemas de formato código
```bash
python automate/vnm_automate.py code-format    # Formatear automáticamente
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
