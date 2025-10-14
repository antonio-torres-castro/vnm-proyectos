# Referencia Rápida - Orquestador VNM

## 🚀 Comandos Esenciales
```bash
python vnm.py           # Verificar estado
python vnm.py up        # Iniciar entorno
python vnm.py down      # Terminar entorno
python vnm.py restart   # Reiniciar
python vnm.py clean     # Regenerar completo
```

## 📊 Logs y Diagnóstico
```bash
python vnm.py logs              # Todos los logs
python vnm.py logs backend      # Solo backend
python vnm.py logs postgres     # Solo database
python vnm.py diagnosticar      # Diagnóstico detallado
```

## 💾 Backup y Mantenimiento
```bash
python vnm.py backup            # Backup manual
python devtools/orquestador_desarrollo.py --help # Ayuda completa
```

## 🌐 URLs de Desarrollo
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **Backend Docs**: http://localhost:8000/docs
- **Debug Server**: localhost:5678

## 🔧 Debugging en VS Code
1. `python vnm.py up`
2. `code .`
3. Presionar **F5** → "Backend: FastAPI Docker Debug"

## 🚨 Solución de Problemas
```bash
# Si hay errores
python vnm.py logs [servicio]

# Regenerar completamente
python vnm.py clean

# Validar configuración
python devtools/validar_orquestador.py
```

## 📁 Archivos Importantes
- `orquestador_desarrollo.py` - Programa principal
- `desarrollo.py` - Comandos rápidos
- `docker-compose.debug.yml` - Configuración desarrollo
- `database/backups/` - Backups automáticos
