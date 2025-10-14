# Configuración de Debug VS Code - CORREGIDA ✅

## Problema Resuelto
El error **"Attribute 'request' is missing from chosen debug configuration"** ha sido corregido.

## 🔧 Configuraciones de Debug Disponibles

### 1. **Frontend Debug**
- **Tipo**: Microsoft Edge debugging
- **Puerto**: http://localhost:3000
- **Uso**: Depura solo el frontend React

### 2. **Backend Debug** 
- **Tipo**: Python debugging
- **Archivo**: backend/app/main.py
- **Uso**: Depura solo el backend FastAPI

### 3. **FullStack Debug - Ambos simultáneamente** ⭐
- **Tipo**: Python con preLaunchTask
- **Funcionalidad**: Inicia el entorno completo y depura el backend
- **Uso**: **Esta es la configuración que necesitas para FullStack**

### 4. **FullStack Debug - Compound**
- **Tipo**: Compound (ejecuta Backend + Frontend)
- **Uso**: Alternativa para debugging simultáneo

## 📋 Pasos para Usar FullStack Debug

### Opción 1: FullStack Debug - Ambos simultáneamente (Recomendado)
1. Presiona **F5** 
2. Selecciona **"FullStack Debug - Ambos simultáneamente"**
3. VS Code ejecutará automáticamente:
   - `python devtools/orquestador_desarrollo.py iniciar`
   - Iniciará el backend en modo debug
   - Podrás poner breakpoints en el código Python

### Opción 2: FullStack Debug - Compound  
1. Presiona **F5**
2. Selecciona **"FullStack Debug - Compound"**
3. VS Code ejecutará ambos debuggers simultáneamente

## 🛠️ Cambios Realizados

### `.vscode/launch.json`
- ✅ Eliminado conflicto en preLaunchTask
- ✅ Cambiado de Chrome a Microsoft Edge debugging
- ✅ Agregada configuración específica "FullStack Debug - Ambos simultáneamente"
- ✅ Mejoradas las rutas de source maps

### `.vscode/tasks.json`
- ✅ Optimizada la tarea "start-fullstack-environment"
- ✅ Mejorado el problemMatcher para detectar cuando el entorno está listo

### `.vscode/extensions.json`
- ✅ Eliminada extensión obsoleta `vscode-chrome-debug`
- ✅ Agregadas extensiones modernas: `js-debug`, `debugpy`, `vscode-edge-devtools`

### `.vscode/settings.json`
- ✅ Agregadas configuraciones específicas para debugging
- ✅ Configurado terminal por defecto para Windows (PowerShell)

## 🚀 Cómo Probar

1. **Instala las extensiones recomendadas** (VS Code te preguntará automáticamente)
2. **Presiona F5**
3. **Selecciona "FullStack Debug - Ambos simultáneamente"**
4. **Espera** a que aparezca el mensaje: "Entorno iniciado correctamente"
5. **Pon breakpoints** en tu código Python
6. **Navega** a http://localhost:3000 para ver el frontend

## ✅ Verificación
- ❌ Error anterior: "Attribute 'request' is missing"  
- ✅ **CORREGIDO**: Todas las configuraciones tienen `request` definido
- ✅ **FUNCIONAL**: El debugging FullStack ahora debe funcionar sin errores

## 📝 Notas Importantes
- La configuración **"FullStack Debug - Ambos simultáneamente"** es la más robusta
- Si prefieres el compound, usa **"FullStack Debug - Compound"** 
- Asegúrate de tener Docker Desktop ejecutándose
- El frontend se abrirá automáticamente en Microsoft Edge

---
**Configuración actualizada el**: 2025-10-14 20:22:42
