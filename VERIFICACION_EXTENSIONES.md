# 🔧 Verificación de Extensiones y Formateo Automático

## ✅ Problemas Corregidos

### 1. **Configuración Black Formatter**
- ✅ Migrado de `python.formatting.provider` (obsoleto) a `ms-python.black-formatter`
- ✅ Configurado `editor.formatOnSave: true` en backend
- ✅ Unificado límite de línea a **79 caracteres** en todas las configuraciones
- ✅ Agregado configuración específica por lenguaje `[python]`

### 2. **Configuraciones Actualizadas**

#### **Backend Settings** (`vscode-config/backend/settings.json`)
```json
{
    "[python]": {
        "editor.defaultFormatter": "ms-python.black-formatter",
        "editor.formatOnSave": true
    },
    "black-formatter.args": [
        "--line-length=79"
    ]
}
```

#### **Root Settings** (`vscode-config/root/settings.json`)  
```json
{
    "[python]": {
        "editor.defaultFormatter": "ms-python.black-formatter",
        "editor.formatOnSave": true,
        "editor.rulers": [79]
    },
    "black-formatter.args": [
        "--line-length=79"
    ]
}
```

## 🧪 Cómo Verificar que Funciona

### **Paso 1: Ejecutar Setup**
```bash
# Linux/Mac
bash setup-vscode-debug.sh

# Windows
./setup-vscode-debug.ps1
```

### **Paso 2: Abrir VS Code y Verificar Extensiones**
```bash
code .
```

**Extensiones requeridas que deben instalarse:**
- `ms-python.black-formatter` ✅
- `ms-python.flake8` ✅
- `ms-python.mypy-type-checker` ✅

### **Paso 3: Probar Formateo Automático**

1. **Abrir archivo de prueba:**
   ```bash
   code test-black-formatting.py
   ```

2. **Verificar que las líneas están sin formatear** (más de 79 caracteres)

3. **Guardar el archivo** (`Ctrl+S` o `Cmd+S`)

4. **Verificar que se formateó automáticamente:**
   - Las líneas largas deben dividirse
   - Los parámetros de función deben estar en líneas separadas
   - Las listas/diccionarios largos deben formatearse

### **Paso 4: Verificar Configuración VS Code**

**Abrir configuración** (`Ctrl+,`) y verificar:

1. **Python › Formatting: Provider** = `ms-python.black-formatter`
2. **Editor: Format On Save** = ✅ habilitado
3. **Black-formatter › Args** = `["--line-length=79"]`

## 🔍 Troubleshooting

### **Si Black no formatea al guardar:**

1. **Verificar extensión instalada:**
   ```
   Ctrl+Shift+X → buscar "ms-python.black-formatter"
   ```

2. **Verificar configuración:**
   ```
   Ctrl+Shift+P → "Python: Select Interpreter"
   ```

3. **Recargar VS Code:**
   ```
   Ctrl+Shift+P → "Developer: Reload Window"
   ```

4. **Verificar Output de Black:**
   ```
   View → Output → seleccionar "Python" o "Black Formatter"
   ```

### **Si aparecen errores de Python interpreter:**

1. **Configurar interpreter correcto:**
   ```
   Ctrl+Shift+P → "Python: Select Interpreter"
   → Seleccionar: ./backend/venv/bin/python
   ```

2. **Verificar que el venv existe:**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # o
   venv\Scripts\activate     # Windows
   pip install -r requirements.txt
   ```

## 📁 Archivos de Configuración Actualizados

- ✅ `vscode-config/backend/settings.json`
- ✅ `vscode-config/root/settings.json`  
- ✅ `setup-vscode-debug.ps1`
- ✅ `setup-vscode-debug.sh`

## 🎯 Resultado Esperado

Después de aplicar estos cambios, **al guardar cualquier archivo `.py`**:

1. **Formateo automático** con Black (79 caracteres)
2. **Organización de imports** automática
3. **Detección de errores** con Flake8 y Mypy
4. **Rulers visuales** en columna 79

## ⚡ Comandos Útiles

```bash
# Formatear manualmente un archivo
Ctrl+Shift+P → "Format Document"

# Organizar imports manualmente  
Ctrl+Shift+P → "Python: Sort Imports"

# Ver problemas detectados
Ctrl+Shift+M (Problems panel)
```
