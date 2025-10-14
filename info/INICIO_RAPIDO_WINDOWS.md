# 🚀 Inicio Rápido - Windows

## 🎯 ¡EMPIEZA EN 3 PASOS!

### 📂 Paso 1: Abrir Terminal en tu Proyecto
```cmd
# Navegar al directorio de tu proyecto
cd C:\ruta\a\tu\proyecto\vnm
```

### 🔧 Paso 2: Elegir tu Terminal Preferida

#### 🟦 **Opción A: PowerShell (RECOMENDADO)**
```powershell
# Cargar comandos de desarrollo
. .\comandos-desarrollo.ps1

# Ver comandos disponibles
Show-DevHelp
```

#### 🟨 **Opción B: Command Prompt (CMD)**
```cmd
# Ver comandos disponibles
comandos-desarrollo.bat help
```

### 🚀 Paso 3: ¡Desarrollar!

#### PowerShell:
```powershell
Dev-Start     # Iniciar entorno
Dev-Status    # Verificar estado
# ¡Ya puedes desarrollar!
```

#### CMD:
```cmd
comandos-desarrollo.bat start    # Iniciar entorno
comandos-desarrollo.bat status   # Verificar estado
# ¡Ya puedes desarrollar!
```

---

## 🎨 DEPURACIÓN EN VS CODE

### **¡Súper Fácil!**
1. **Abrir VS Code** en tu proyecto
2. **Presionar F5**
3. **Seleccionar "FullStack Debug"**
4. **¡Automático!** VS Code inicia todo

---

## 🌐 URLs DE TU APLICACIÓN

Después de `Dev-Start`, abre en tu navegador:

| Servicio | URL | Descripción |
|----------|-----|-------------|
| **Frontend** | http://localhost:3000 | Tu aplicación React |
| **Backend API** | http://localhost:8000 | API FastAPI |
| **API Docs** | http://localhost:8000/docs | Documentación interactiva |
| **PgAdmin** | http://localhost:5050 | Admin BD (opcional) |

---

## 🛑 AL FINAL DEL DÍA

### PowerShell:
```powershell
Dev-Stop    # Para todo y crea backup automático
```

### CMD:
```cmd
comandos-desarrollo.bat stop    # Para todo y crea backup automático
```

---

## 🆘 ¿PROBLEMAS?

### **¿Docker no funciona?**
1. Verificar que Docker Desktop esté ejecutándose
2. `docker --version` debe mostrar la versión

### **¿Python no funciona?**
1. Verificar instalación: `python --version`
2. Si no está instalado, descargar de python.org

### **¿El entorno no responde?**
```powershell
# PowerShell
Dev-Restart

# CMD
comandos-desarrollo.bat restart
```

### **¿Necesitas ayuda completa?**
- **PowerShell**: `Show-DevHelp`
- **CMD**: `comandos-desarrollo.bat help`
- **Documentación**: Lee <filepath>FLUJO_DESARROLLO_WINDOWS.md</filepath>

---

## 📋 COMANDOS ESENCIALES

### PowerShell (Recomendado)

| Lo que quieres hacer | Comando |
|---------------------|---------|
| Ver todos los comandos | `Show-DevHelp` |
| Iniciar desarrollo | `Dev-Start` |
| Ver estado | `Dev-Status` |
| Ver logs | `Dev-Logs` |
| Verificar salud | `Dev-Health` |
| Parar (con backup) | `Dev-Stop` |
| Limpiar todo | `Dev-Stop-Clean` |
| Abrir API en navegador | `Dev-Open api` |
| Abrir Frontend | `Dev-Open frontend` |

### Command Prompt (CMD)

| Lo que quieres hacer | Comando |
|---------------------|---------|
| Ver todos los comandos | `comandos-desarrollo.bat help` |
| Iniciar desarrollo | `comandos-desarrollo.bat start` |
| Ver estado | `comandos-desarrollo.bat status` |
| Ver logs | `comandos-desarrollo.bat logs` |
| Verificar salud | `comandos-desarrollo.bat health` |
| Parar (con backup) | `comandos-desarrollo.bat stop` |
| Limpiar todo | `comandos-desarrollo.bat stop-clean` |
| Abrir API en navegador | `comandos-desarrollo.bat open api` |
| Abrir Frontend | `comandos-desarrollo.bat open frontend` |

---

## ✅ VERIFICAR QUE TODO FUNCIONA

### 1. ¿Docker está listo?
```cmd
docker --version
docker-compose --version
```

### 2. ¿Python está listo?
```cmd
python --version
```

### 3. ¿Los archivos están ahí?
- ✅ `comandos-desarrollo.ps1` existe
- ✅ `comandos-desarrollo.bat` existe  
- ✅ `devtools/orquestador_desarrollo.py` existe
- ✅ `.vscode/launch.json` existe

### 4. ¿Funciona el inicio?
```powershell
# PowerShell
Dev-Start

# CMD
comandos-desarrollo.bat start
```

Si todo anterior funciona: **¡ESTÁS LISTO! 🎉**

---

## 🎯 TU FLUJO DIARIO

```
1. Abrir terminal en tu proyecto
   ↓
2. Cargar comandos (solo PowerShell):
   . .\comandos-desarrollo.ps1
   ↓
3. Iniciar desarrollo:
   Dev-Start (o comandos-desarrollo.bat start)
   ↓
4. ¡DESARROLLAR! 🎨
   (VS Code F5 para depuración)
   ↓
5. Al terminar:
   Dev-Stop (o comandos-desarrollo.bat stop)
```

---

## 🎊 ¡YA ESTÁS LISTO PARA DESARROLLAR!

**¿Siguiente paso?** 
- Ejecuta `Dev-Start` y abre http://localhost:3000
- Para depuración: Abre VS Code y presiona F5

**¿Dudas?** 
- Lee la documentación completa en <filepath>FLUJO_DESARROLLO_WINDOWS.md</filepath>

---

**Configurado para**: Windows con Docker Desktop  
**Tu flujo**: PowerShell + VS Code + Docker  
**Estado**: ✅ **¡LISTO PARA DESARROLLAR!**
