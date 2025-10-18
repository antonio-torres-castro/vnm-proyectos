#!/bin/sh

# Script de inicio para debugging del frontend
echo "🔧 Iniciando Vite con debugging habilitado..."
echo "📍 NODE_OPTIONS: --inspect=0.0.0.0:24678"

# Forzar NODE_OPTIONS y ejecutar Vite
NODE_OPTIONS="--inspect=0.0.0.0:24678" exec npm run dev:debug