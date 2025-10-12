# Solución Integrada - Problema pgAdmin

## Problema Solucionado
**Error**: `PermissionError: [Errno 1] Operation not permitted: '/var/lib/pgadmin/pgadmin4.db'`

**Causa**: Problema de permisos en Windows cuando pgAdmin intenta ejecutar `chmod` en archivos ubicados en bind mounts.

## Cambios Realizados

### 1. Modificación en docker-compose.yml
**Antes:**
```yaml
volumes:
  - ./database/pgadmin-data:/var/lib/pgadmin
```

**Después:**
```yaml
volumes:
  - pgadmin_data:/var/lib/pgadmin
```

**Beneficio**: Uso de volumen nombrado manejado por Docker evita problemas de permisos en Windows.

### 2. Nuevas Funciones en manage-db.ps1

#### `fix-pgadmin`
- **Propósito**: Solucionar automáticamente problemas de permisos de pgAdmin
- **Acción**: 
  - Detiene contenedor problemático
  - Respalda configuración existente
  - Elimina directorio con problemas
  - Reinicia pgAdmin con volumen nombrado
- **Uso**: `.\manage-db.ps1 fix-pgadmin`

#### `clean-pgadmin`
- **Propósito**: Limpieza completa de pgAdmin (reseteo total)
- **Acción**:
  - Elimina completamente contenedor y volumen
  - Recrea pgAdmin desde cero
  - Requiere reconfiguración inicial
- **Uso**: `.\manage-db.ps1 clean-pgadmin`

## Instrucciones de Uso

### Problema Activo de pgAdmin
```powershell
# Navegar al directorio de scripts
cd database\scripts

# Reparación automática (RECOMENDADO)
.\manage-db.ps1 fix-pgadmin

# Si persiste el problema, limpieza completa
.\manage-db.ps1 clean-pgadmin
```

### Verificación Post-Reparación
1. **Acceder a pgAdmin**: http://localhost:8081
2. **Credenciales**:
   - Email: `admin@monitoreo.cl`
   - Password: `admin123`
3. **Verificar logs**: `.\manage-db.ps1 logs`

### Comandos de Diagnóstico
```powershell
# Ver estado de servicios
.\manage-db.ps1 status

# Ver logs específicos de pgAdmin
docker logs monitoreo_pgadmin

# Ver contenedores activos
docker ps
```

## Ventajas de la Solución

### ✅ Robustez
- **Volumen nombrado**: Docker maneja automáticamente los permisos
- **Multiplataforma**: Funciona en Windows, Linux y macOS
- **Persistencia**: Los datos se mantienen entre reinicios

### ✅ Automatización
- **Reparación automática**: Un comando soluciona el problema
- **Respaldo automático**: Preserva configuración existente
- **Integración**: Funciones integradas en el sistema existente

### ✅ Mantenimiento
- **Documentación actualizada**: Instrucciones claras y específicas
- **Opciones múltiples**: Reparación y limpieza completa
- **Diagnóstico**: Herramientas para troubleshooting

## Compatibilidad
- ✅ **Windows 10/11**: Solución principal para este SO
- ✅ **Docker Desktop**: Compatible con versiones actuales
- ✅ **WSL2**: Funciona en ambiente Windows Subsystem for Linux
- ✅ **Proyectos existentes**: No afecta datos de PostgreSQL ni backend

## Notas Técnicas
- El volumen `pgadmin_data` se crea automáticamente
- Los datos de configuración de servidores se mantienen en archivos externos
- El cambio es retrocompatible con instalaciones existentes
- Los backups de pgAdmin se crean automáticamente antes de reparaciones
