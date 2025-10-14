# SOLUCION LIMPIA - RECREACION DE BASE DE DATOS

## PROBLEMA RESUELTO
- Error: `duplicate key value violates unique constraint "usuario_pkey"`
- Causa: Script SQL creaba usuario administrador con ID fijo, causando conflicto con secuencia

## SOLUCION IMPLEMENTADA

### 1. ARCHIVOS CORREGIDOS
- `backend/app/models/usuario.py` - Agregado `autoincrement=True`
- `backend/app/api/usuarios.py` - Endpoint `/crear-admin` con manejo robusto de errores
- `database/init-data/02-datos-autenticacion.sql` - ELIMINADA creacion de usuario admin

### 2. SCRIPTS ELIMINADOS
Todos los scripts de parches fueron eliminados:
- reparar_secuencia_*.py
- fix_sequence.*
- verificar-sistema-completo.ps1
- verificar-database.ps1
- formatear-codigo.ps1
- reinicializar-database.ps1

### 3. SCRIPT DE RECREACION LIMPIA
- `recrear_base_datos.py` - Script Python para recreacion completa

## PROCESO CORRECTO

### Opcion 1: Recreacion Automatica (Recomendado)
```bash
python recrear_base_datos.py
```

### Opcion 2: Recreacion Manual
```bash
# 1. Detener contenedores
docker-compose -f docker-compose.debug.yml down

# 2. Eliminar volumen (limpieza completa)
docker volume rm vnm-proyectos_postgres_data_debug

# 3. Levantar servicios (scripts de BD se ejecutan automaticamente)
docker-compose -f docker-compose.debug.yml up -d
```

### Crear Usuario Administrador
```bash
# Esperar que backend este listo, luego:
curl -X POST http://localhost:8000/api/v1/usuarios/crear-admin
```

### Verificar
```bash
# Login en Swagger UI: http://localhost:8000/docs
# Credenciales: admin@monitoreo.cl / admin123

# Frontend: http://localhost:3000
```

## VENTAJAS DE ESTA SOLUCION

1. **Limpia**: No hay parches, solo recreacion completa
2. **Eficiente**: Con solo parametria, recrear es mas rapido que parchear
3. **Mantenible**: Scripts SQL limpios sin usuarios hardcodeados
4. **Robusta**: Endpoint API crea usuario usando logica del sistema
5. **Consistente**: Backend maneja la creacion, no scripts externos

## NOTAS TECNICAS

- PostgreSQL ejecuta automaticamente scripts en `/docker-entrypoint-initdb.d/`
- Tabla `seguridad.usuario` queda vacia inicialmente
- Secuencia `usuario_id_seq` empieza correctamente desde 1
- Endpoint `/crear-admin` es publico (sin autenticacion) para bootstrap
- Solo funciona una vez (verifica que no exista admin)
