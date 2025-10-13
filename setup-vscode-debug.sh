#!/bin/bash
# Script de configuración para debugging en VS Code - Linux/Mac

echo "🔧 Configurando entorno de debugging de VS Code..."

# Función para crear directorio si no existe
create_dir_if_not_exists() {
    if [ ! -d "$1" ]; then
        mkdir -p "$1"
        echo "📁 Creado directorio: $1"
    fi
}

# Función para copiar archivos con verificación
copy_with_verification() {
    if [ -f "$1" ]; then
        cp -f "$1" "$2"
        echo "✅ Copiado: $1 -> $2"
    else
        echo "⚠️  Archivo fuente no encontrado: $1"
    fi
}

# Verificar que estamos en el directorio correcto
if [ ! -d "vscode-config" ]; then
    echo "❌ Error: Directorio 'vscode-config' no encontrado"
    echo "   Asegúrate de ejecutar este script desde la raíz del proyecto vnm-proyectos"
    exit 1
fi

# Crear directorios .vscode
echo "📁 Creando directorios .vscode..."
create_dir_if_not_exists ".vscode"
create_dir_if_not_exists "backend/.vscode"
create_dir_if_not_exists "frontend/.vscode"

# Copiar configuraciones del directorio raíz
echo "📋 Copiando configuraciones del directorio raíz..."
copy_with_verification "vscode-config/root/launch.json" ".vscode/launch.json"
copy_with_verification "vscode-config/root/tasks.json" ".vscode/tasks.json"
copy_with_verification "vscode-config/root/extensions.json" ".vscode/extensions.json"
copy_with_verification "vscode-config/root/settings.json" ".vscode/settings.json"

# Copiar configuraciones del backend
echo "🐍 Copiando configuraciones del backend..."
copy_with_verification "vscode-config/backend/launch.json" "backend/.vscode/launch.json"
copy_with_verification "vscode-config/backend/settings.json" "backend/.vscode/settings.json"

# Copiar configuraciones del frontend
echo "⚛️ Copiando configuraciones del frontend..."
copy_with_verification "vscode-config/frontend/launch.json" "frontend/.vscode/launch.json"
copy_with_verification "vscode-config/frontend/extensions.json" "frontend/.vscode/extensions.json"

echo ""
echo "🎉 ¡Configuración completada exitosamente!"
echo ""
echo "📝 Próximos pasos:"
echo "1. Abrir VS Code: code ."
echo "2. Instalar extensiones recomendadas cuando VS Code lo sugiera"
echo "3. Ejecutar task 'Debug: Full Environment Setup' para iniciar todo"
echo ""
