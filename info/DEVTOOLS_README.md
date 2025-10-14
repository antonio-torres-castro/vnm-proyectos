# VNM Proyectos - Herramientas de Desarrollo

## 🏗️ **Estructura Organizada del Proyecto**

```
vnm-proyectos/
├── backend/                    # Código del backend FastAPI
├── frontend/                   # Código del frontend React  
├── database/                   # Scripts y datos de base de datos
├── devtools/                   # 🔧 Herramientas de desarrollo
│   ├── orquestador_desarrollo.py   # Orquestador principal
│   ├── desarrollo.py               # Comandos internos
│   ├── validar_orquestador.py      # Validación del entorno
│   ├── instalar_orquestador.py     # Instalador
│   └── documentación/...           # Docs completas
├── vnm.py                      # 🚀 Script de acceso principal
├── docker-compose.yml          # Configuración producción
├── docker-compose.debug.yml    # Configuración desarrollo
└── inicio_rapido.sh           # Script de inicio rápido
```

## 🚀 **Comandos Principales (Desde la Raíz)**

### ⚡ **Instalación Inicial**
```bash
# 1. Instalar dependencia requerida
pip install requests

# 2. Configurar herramientas (ejecutar una sola vez)
python devtools/instalar_orquestador.py

# 3. Validar configuración
python devtools/validar_orquestador.py
```

### 🎮 **Comandos de Desarrollo Diario**
```bash
# Verificar estado
python vnm.py

# Iniciar entorno completo  
python vnm.py up

# Terminar entorno (con backup)
python vnm.py down

# Reiniciar entorno
python vnm.py restart

# Regenerar completamente
python vnm.py clean

# Ver logs
python vnm.py logs [servicio]

# Backup manual
python vnm.py backup

# Ayuda
python vnm.py help
```

### ⚡ **Script de Inicio Ultra-Rápido**
```bash
# Una sola línea para iniciar todo
./inicio_rapido.sh
# o
bash inicio_rapido.sh
```

## 🔧 **Solución de Problemas**

### ❌ **Error: "No module named 'requests'"**
```bash
# Solución:
pip install requests
```

### ❌ **Error: "No se encontró vnm.py"**
```bash
# Verificar que estás en la raíz del proyecto
pwd
ls vnm.py
```

### ❌ **Error: "Docker no está ejecutándose"**
```bash
# Windows:
# Iniciar Docker Desktop

# Linux:
sudo systemctl start docker
```

### ❌ **Error: "Sin permisos para Docker"**
```bash
# Linux:
sudo usermod -aG docker $USER
# Luego reiniciar sesión
```

## 🎯 **Flujo de Trabajo Recomendado**

### **Desarrollo Diario**
```bash
# 1. Iniciar día
python vnm.py up

# 2. Abrir VS Code y comenzar debugging
code .
# Presionar F5 → "Backend: FastAPI Docker Debug"

# 3. Desarrollar...

# 4. Al final del día
python vnm.py down
```

### **Cuando hay Problemas**
```bash
# 1. Ver logs del servicio problemático
python vnm.py logs backend
python vnm.py logs postgres

# 2. Si persiste, regenerar completamente
python vnm.py clean
```

### **Migración desde PowerShell**
| Script PowerShell Anterior | Comando Nuevo |
|---------------------------|---------------|
| `inicio-desarrollo.ps1` | `python vnm.py up` |
| `cerrar-desarrollo.ps1` | `python vnm.py down` |
| `cerrar-desarrollo.ps1 -LimpiarCompleto` | `python vnm.py clean` |

## 🌐 **URLs de Desarrollo**

Después de ejecutar `python vnm.py up`:

| Servicio | URL | Descripción |
|----------|-----|-------------|
| **Frontend** | http://localhost:3000 | Aplicación React |
| **Backend API** | http://localhost:8000 | API FastAPI |
| **Backend Docs** | http://localhost:8000/docs | Documentación Swagger |
| **PostgreSQL** | localhost:5432 | Base de datos |
| **Debug Server** | localhost:5678 | Puerto de debugging VS Code |

## 📁 **Archivos de las Herramientas**

### En `/devtools/`:
- `orquestador_desarrollo.py` - Orquestador principal completo
- `desarrollo.py` - Comandos simplificados
- `validar_orquestador.py` - Validación del entorno
- `instalar_orquestador.py` - Configuración inicial
- `ORQUESTADOR_README.md` - Documentación completa
- `EJEMPLO_SALIDA_ORQUESTADOR.md` - Ejemplos de uso
- `REFERENCIA_RAPIDA.md` - Guía de referencia

### En la raíz:
- `vnm.py` - Script de acceso principal
- `inicio_rapido.sh` - Inicio con una línea
- `vnm_aliases.sh` - Aliases de bash

## 💾 **Backup Automático**

- **Ubicación**: `database/backups/`
- **Formato**: `backup_YYYYMMDD_HHMMSS.sql.zip`
- **Automático**: Antes de `down` y `clean`
- **Retención**: Últimos 10 backups

## ⚙️ **Configuración Avanzada**

### **Usar Aliases de Bash**
```bash
# Cargar aliases
source vnm_aliases.sh

# Usar comandos cortos
vnm-up      # = python vnm.py up
vnm-down    # = python vnm.py down
vnm-status  # = python vnm.py
```

### **Validación del Entorno**
```bash
# Verificar que todo está bien configurado
python devtools/validar_orquestador.py
```

### **Modo Verboso**
```bash
# Para debugging del orquestador
python devtools/orquestador_desarrollo.py diagnosticar --verboso
```

## 🎉 **Beneficios de la Nueva Estructura**

1. ✅ **Organización Clara**: Herramientas separadas del código del proyecto
2. ✅ **Acceso Simple**: Un solo comando `python vnm.py` desde cualquier lugar
3. ✅ **Sin Contaminación**: Los archivos de desarrollo no interfieren con el proyecto
4. ✅ **Mantenimiento Fácil**: Todas las herramientas en una carpeta dedicada
5. ✅ **Escalabilidad**: Fácil agregar nuevas herramientas sin desordenar
6. ✅ **Python Puro**: Sin PowerShell, sin caracteres especiales

## 🚀 **¡Listo Para Usar!**

```bash
# Para empezar inmediatamente:
pip install requests
python vnm.py up
code .
# Presionar F5 en VS Code
```

---

> 💡 **Tip**: Para cualquier duda, ejecuta `python vnm.py help` o revisa la documentación completa en `devtools/ORQUESTADOR_README.md`
