#!/bin/bash
# Script de Inicio Rápido VNM-Proyectos

echo "🚀 Iniciando VNM-Proyectos..."

# Verificar que estamos en el directorio correcto
if [ ! -f "vnm.py" ]; then
    echo "❌ Error: No se encontró vnm.py"
    echo "💡 Asegúrate de estar en el directorio raíz del proyecto"
    exit 1
fi

# Iniciar entorno
python vnm.py up

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
    echo "   • Ver estado:   python vnm.py"
    echo "   • Ver logs:     python vnm.py logs [servicio]"
    echo "   • Terminar:     python vnm.py down"
else
    echo "❌ Error iniciando el entorno"
    echo "💡 Revisa los logs: python desarrollo.py logs"
fi
