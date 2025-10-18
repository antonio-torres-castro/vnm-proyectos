# Automatismos Simplificados

Este directorio contiene solo los scripts esenciales para el desarrollo.

## Scripts Disponibles

### docker_manager.py (en raíz del proyecto)
- Manejo de containers PostgreSQL y pgAdmin únicamente
- Comandos: start, stop, restart, status, logs, clean
- Frontend y backend corren localmente

### extensiones_vscode.py  
- Instalación automática de extensiones recomendadas de VS Code
- Lista predefinida de extensiones esenciales

### utilidades.py
- Funciones de utilidad compartidas
- Verificaciones de sistema
- Helpers para otros scripts

## Uso

```bash
# Manejar containers de base de datos
python docker_manager.py start

# Instalar extensiones de VS Code
python automate/extensiones_vscode.py

# Ver utilidades disponibles
python automate/utilidades.py --help
```

## Desarrollo Local Simplificado

- **Base de datos**: PostgreSQL + pgAdmin en Docker
- **Backend**: Python/FastAPI corriendo localmente
- **Frontend**: React/Vite corriendo localmente

## Scripts Removidos

Los siguientes scripts fueron removidos por usar Docker para frontend/backend:
- apply_complete_debugging_fix.py (era específico para Docker debugging)
- fix_containers_compatibility.py (ya no usamos containers para frontend/backend)
- fix_debug_containers.py (ya no usamos containers para frontend/backend)
- test_encoding_concept.py (era específico para comandos Docker)

Scripts previamente removidos:
- crear_entornos_virtuales.py (reemplazado por guía manual)
- inicio_desarrollo.py (reemplazado por docker_manager.py)
- cerrar_desarrollo.py (reemplazado por docker_manager.py) 
- configurar_proyecto_completo.py (reemplazado por README_CONFIGURACION.md)
- verificar_configuracion_completa.py (innecesario con configuración manual)
- validar_extensiones_vscode.py (integrado en extensiones_vscode.py)
