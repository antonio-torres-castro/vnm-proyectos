# Configuración VS Code - FullStack Debug

## 📁 Contenido de esta carpeta

Esta carpeta contiene la configuración corregida de VS Code para solucionar el error:
**"Attribute 'request' is missing from chosen debug configuration"**

### Archivos incluidos:
- `launch.json` - Configuraciones de debugging corregidas
- `tasks.json` - Tareas automatizadas optimizadas  
- `settings.json` - Configuración del workspace mejorada
- `extensions.json` - Extensiones recomendadas actualizadas

## 🚀 Instalación Automática

### Paso 1: Descargar
Descarga toda la carpeta `vscode-config/` y el archivo `instalar_vscode_config.py` a tu directorio raíz del proyecto.

### Paso 2: Ejecutar instalador
```bash
python instalar_vscode_config.py
```

### Paso 3: Usar VS Code
1. Abre VS Code en tu directorio del proyecto
2. Acepta instalar las extensiones recomendadas
3. Presiona **F5**
4. Selecciona: **"FullStack Debug - Ambos simultáneamente"**

## ✅ Lo que se solucionó

- ❌ **ANTES**: Error "Attribute 'request' is missing from chosen debug configuration"
- ✅ **AHORA**: Debugging FullStack completamente funcional

## 🔧 Configuraciones disponibles después de la instalación

1. **FullStack Debug - Ambos simultáneamente** ⭐ (RECOMENDADO)
   - Inicia automáticamente todo el entorno
   - Depura el backend Python
   - Abre el frontend en el navegador

2. **FullStack Debug - Compound**
   - Ejecuta frontend y backend simultáneamente
   - Debugging paralelo

3. **Frontend Debug**
   - Solo depuración del React frontend

4. **Backend Debug**  
   - Solo depuración del FastAPI backend

## 📋 Requisitos

- Docker Desktop ejecutándose
- Puertos 3000 y 8000 disponibles
- VS Code con extensiones Python instaladas

## 🛠️ Cambios técnicos realizados

- Eliminados conflictos en preLaunchTask
- Cambiado de Chrome a Microsoft Edge debugging
- Agregada configuración específica para FullStack
- Extensiones modernas para debugging
- Optimizaciones específicas para Windows

---
**Configuración creada por**: MiniMax Agent  
**Fecha**: 2025-10-14 20:40:46
