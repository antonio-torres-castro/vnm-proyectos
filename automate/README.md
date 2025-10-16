# Automatismos Simplificados

Este directorio contiene solo los scripts esenciales para el desarrollo.

## Scripts Disponibles

### docker_manager.py (en raiz del proyecto)
- Manejo completo de containers Docker
- Comandos: start, stop, restart, status, logs, clean
- Soporte para modo debug

### extensiones_vscode.py  
- Instalacion automatica de extensiones recomendadas de VS Code
- Lista predefinida de extensiones esenciales

### utilidades.py
- Funciones de utilidad compartidas
- Verificaciones de sistema
- Helpers para otros scripts

## Uso

```bash
# Manejar containers Docker
python docker_manager.py start

# Instalar extensiones de VS Code
python automate/extensiones_vscode.py

# Ver utilidades disponibles
python automate/utilidades.py --help
```

## Scripts Removidos

Los siguientes scripts fueron removidos por complejidad innecesaria:
- crear_entornos_virtuales.py (reemplazado por guia manual)
- inicio_desarrollo.py (reemplazado por docker_manager.py)
- cerrar_desarrollo.py (reemplazado por docker_manager.py) 
- configurar_proyecto_completo.py (reemplazado por README_CONFIGURACION.md)
- verificar_configuracion_completa.py (innecesario con configuracion manual)
- validar_extensiones_vscode.py (integrado en extensiones_vscode.py)

Los archivos originales estan respaldados en `automate_backup_original/`.