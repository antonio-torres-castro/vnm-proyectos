#!/bin/bash
# Script de Inicio Rápido VNM-Proyectos

echo "🚀 Iniciando VNM-Proyectos..."

# Verificar que estamos en el directorio correcto
if [ ! -f "desarrollo.py" ]; then
    echo "❌ Error: No se encontró desarrollo.py"
    echo "💡 Asegúrate de estar en el directorio del proyecto"
    exit 1
fi

# Iniciar entorno
python desarrollo.py up

# Si todo salió bien, mostrar información útil
if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 ¡Entorno iniciado correctamente!"
    echo ""
    echo "📱 URLs disponibles:"
    echo "   • Frontend:     http://localhost:3000"
    echo "   • Backend API:  http://localhost:8000"
    echo "   • Backend Docs: http://localhost:8000/docs"
    echo ""
    echo "🔧 Para debugging en VS Code:"
    echo "   1. Abrir VS Code: code ."
    echo "   2. Presionar F5 → 'Backend: FastAPI Docker Debug'"
    echo ""
    echo "📊 Comandos útiles:"
    echo "   • Ver estado:   python desarrollo.py"
    echo "   • Ver logs:     python desarrollo.py logs [servicio]"
    echo "   • Terminar:     python desarrollo.py down"
else
    echo "❌ Error iniciando el entorno"
    echo "💡 Revisa los logs: python desarrollo.py logs"
fi
