#!/bin/bash
# Script para configurar debugging de VS Code
# Ejecutar desde la raíz del proyecto vnm-proyectos

echo "🔧 Configurando entorno de debugging de VS Code..."

# Crear directorios .vscode si no existen
directories=(".vscode" "backend/.vscode" "frontend/.vscode")

for dir in "${directories[@]}"; do
    if [ ! -d "$dir" ]; then
        mkdir -p "$dir"
        echo "✅ Creado: $dir"
    else
        echo "📁 Ya existe: $dir"
    fi
done

# Copiar configuraciones desde vscode-config a .vscode
echo "📋 Copiando configuraciones..."

# Raíz del proyecto
if [ -d "vscode-config/root" ]; then
    cp -r vscode-config/root/* .vscode/
    echo "✅ Copiado: vscode-config/root/* -> .vscode/"
fi

# Backend
if [ -d "vscode-config/backend" ]; then
    cp -r vscode-config/backend/* backend/.vscode/
    echo "✅ Copiado: vscode-config/backend/* -> backend/.vscode/"
fi

# Frontend  
if [ -d "vscode-config/frontend" ]; then
    cp -r vscode-config/frontend/* frontend/.vscode/
    echo "✅ Copiado: vscode-config/frontend/* -> frontend/.vscode/"
fi

# Verificar que los archivos se copiaron correctamente
echo ""
echo "🔍 Verificando configuraciones..."

required_files=(
    ".vscode/launch.json"
    ".vscode/tasks.json"
    ".vscode/settings.json" 
    ".vscode/extensions.json"
    "backend/.vscode/launch.json"
    "backend/.vscode/settings.json"
    "frontend/.vscode/launch.json"
    "frontend/.vscode/settings.json"
)

all_exists=true

for file in "${required_files[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ $file"
    else
        echo "❌ $file"
        all_exists=false
    fi
done

if [ "$all_exists" = true ]; then
    echo ""
    echo "🎉 Configuración de debugging completada exitosamente!"
    echo "📖 Revisa DEBUG_SETUP.md para instrucciones de uso"
    echo ""
    echo "🚀 Próximos pasos:"
    echo "1. Abrir VS Code en esta carpeta: code ."
    echo "2. Instalar extensiones recomendadas"
    echo "3. Iniciar Docker: docker-compose -f docker-compose.debug.yml up -d"
    echo "4. Arreglar login: Ctrl+Shift+P -> Tasks: Run Task -> Fix Admin Password"
    echo "5. Debuggear: Ctrl+Shift+D -> 🚀 Full Stack: Debug Both -> F5"
else
    echo ""
    echo "❌ Algunos archivos no se copiaron correctamente"
    echo "   Revisa los permisos y vuelve a ejecutar el script"
fi

echo ""
echo "📋 Configuraciones disponibles:"
echo "• 🚀 Full Stack: Debug Both - Debuggea backend + frontend"
echo "• 🐍 Backend: FastAPI Docker Debug - Solo backend"
echo "• ⚛️ Frontend: React Chrome Debug - Solo frontend"  
echo "• 🧪 Tests con debugging para ambos proyectos"
