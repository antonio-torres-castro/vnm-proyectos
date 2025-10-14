# Referencia Rápida - Orquestador VNM

## 🚀 Comandos Esenciales
```bash
python desarrollo.py           # Verificar estado
python desarrollo.py up        # Iniciar entorno
python desarrollo.py down      # Terminar entorno
python desarrollo.py restart   # Reiniciar
python desarrollo.py clean     # Regenerar completo
```

## 📊 Logs y Diagnóstico
```bash
python desarrollo.py logs              # Todos los logs
python desarrollo.py logs backend      # Solo backend
python desarrollo.py logs postgres     # Solo database
python desarrollo.py diagnosticar      # Diagnóstico detallado
```

## 💾 Backup y Mantenimiento
```bash
python desarrollo.py backup            # Backup manual
python orquestador_desarrollo.py --help # Ayuda completa
```

## 🌐 URLs de Desarrollo
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **Backend Docs**: http://localhost:8000/docs
- **Debug Server**: localhost:5678

## 🔧 Debugging en VS Code
1. `python desarrollo.py up`
2. `code .`
3. Presionar **F5** → "Backend: FastAPI Docker Debug"

## 🚨 Solución de Problemas
```bash
# Si hay errores
python desarrollo.py logs [servicio]

# Regenerar completamente
python desarrollo.py clean

# Validar configuración
python validar_orquestador.py
```

## 📁 Archivos Importantes
- `orquestador_desarrollo.py` - Programa principal
- `desarrollo.py` - Comandos rápidos
- `docker-compose.debug.yml` - Configuración desarrollo
- `database/backups/` - Backups automáticos
