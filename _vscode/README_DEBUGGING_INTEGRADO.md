# Flujo de Debugging Integrado

## Problema Resuelto

**ANTES**: Los automatismos usaban modo produccion por defecto, sin debugging.
**AHORA**: Todo esta integrado para usar modo debug automaticamente.

## Configuraciones de Debug Disponibles

### 1. FullStack Debug (Smart) - RECOMENDADO
- **Que hace**: Levanta automaticamente el entorno completo en modo debug
- **Debugging**: Se conecta al puerto 5678 del container
- **Uso**: Seleccionar en VS Code Debug panel y presionar F5

### 2. Backend Debug (Container)
- **Que hace**: Se conecta a un container que ya esta ejecutando
- **Uso**: Para cuando el entorno ya esta levantado

### 3. Backend Debug (Local)
- **Que hace**: Ejecuta el backend localmente (sin containers)
- **Uso**: Para desarrollo local rapido

## Tareas Automatizadas

### Tareas Inteligentes (Recomendadas)
- `start-development-environment`: Usa orquestador completo
- `stop-development-environment`: Detiene con backup automatico
- `diagnose-development-environment`: Diagnostico completo

### Tareas Basicas (Legacy)
- `start-containers`: Para debugging basico
- `stop-containers`: Detiene containers basicos

## Comandos Manuales

```bash
# Iniciar entorno completo (modo debug por defecto)
python vnm_automate.py dev-start

# Diagnosticar estado
python vnm_automate.py dev-status

# Detener con backup
python vnm_automate.py dev-stop
```

## Verificacion de Debugging

Despues de ejecutar `FullStack Debug (Smart)`, verificar:

1. **Containers correctos ejecutandose**:
   ```
   vnm_backend_debug     <- Puerto 5678 disponible
   vnm_frontend_debug    <- Con hot reload
   vnm_postgres_debug    <- Base de datos debug
   ```

2. **Puertos disponibles**:
   - Backend API: http://localhost:8000
   - Backend Debug: localhost:5678 (VS Code se conecta aqui)
   - Frontend: http://localhost:3000
   - PostgreSQL: localhost:5432

3. **VS Code conectado**: En la barra de estado debe aparecer "Python Debugger: Connected"

## Solucion de Problemas

**Si aparecen containers de produccion** (monitoreo_*):
```bash
# Detener modo produccion
docker-compose -f docker-compose.yml down

# Iniciar modo debug
python vnm_automate.py dev-start
```

**Si VS Code no se conecta al debugger**:
1. Verificar que el container vnm_backend_debug esta ejecutando
2. Verificar que el puerto 5678 esta disponible
3. Reiniciar la configuracion de debug en VS Code

## Integracion Completa

El flujo esta completamente integrado:
1. VS Code ejecuta la tarea preLaunchTask
2. La tarea levanta el entorno completo en modo debug
3. VS Code se conecta automaticamente al puerto 5678
4. Debugging disponible inmediatamente

No es necesario ejecutar comandos manuales.