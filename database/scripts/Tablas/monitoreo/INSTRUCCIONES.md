# Scripts SQL de Monitoreo - VNM

## ✅ Scripts Creados Exitosamente

### 📁 Archivos Generados

```
database/
├── 00_EJECUTAR_TODOS.sql              (12 KB)  ← 🚀 EJECUTAR ESTE PRIMERO
├── 01_create_schema_monitoreo.sql   (642 B)
├── 02_create_table_dispositivos.sql (4.4 KB)
├── 03_create_table_interfaces.sql   (6.0 KB)
├── 04_create_table_interface_historico.sql (3.7 KB)
├── 05_create_table_dispositivo_historico.sql (3.4 KB)
├── 06_create_triggers_and_functions.sql (5.1 KB)
├── 07_insert_sample_data.sql        (6.7 KB)  ← OPCIONAL
└── README.md                       (8.2 KB)

Total: 9 archivos SQL + 1 README
```

---

## 🚀 Inicio Rápido - 3 Pasos

### Paso 1: Abrir PgAdmin

1. Iniciar **PgAdmin 4**
2. Conectarse a tu servidor PostgreSQL
3. Seleccionar la base de datos donde crearás el esquema

### Paso 2: Ejecutar Script Maestro

1. Click derecho en la base de datos
2. Seleccionar **Query Tool**
3. Abrir archivo: `database/00_EJECUTAR_TODOS.sql`
4. Presionar **F5** o click en "Execute"

### Paso 3: Verificar Creación

El script mostrará el progreso:
```
PASO 1/7: Creando esquema monitoreo...
  ✓ Esquema creado exitosamente

PASO 2/7: Creando tabla dispositivos...
  ✓ Tabla dispositivos creada con 8 índices

...

✓ ESQUEMA DE MONITOREO CREADO EXITOSAMENTE
```

---

## 📊 Estructura Creada

### Tablas Principales (4)

#### 1. **monitoreo.dispositivos**
Catálogo de dispositivos de red

**Campos clave:**
- `devid` (PK) - ID único
- `devname` - Nombre del dispositivo  
- `devip` - IP del dispositivo
- `devstatus` - Estado: 0=No responde, 1=UP, 2=Caído, 5=Fuera
- `enterprise` - Fabricante (Cisco, Huawei, etc.)
- `latitud/longitud` - Geolocalización GPS

**Índices:** 8 optimizados para búsquedas

---

#### 2. **monitoreo.interfaces**
Interfaces con métricas en tiempo real

**Campos clave:**
- `id` (PK) - ID autoincrementable
- `devid` (FK) - Dispositivo padre
- `devif` - ID de interfaz en sistema externo
- `ifstatus` - Estado: 1=UP, 2=Down, 3=Shutdown
- `input/output` - Tráfico en bps
- `ifutil` - Utilización 0-100%
- `ifinerr/ifouterr` - Errores de entrada/salida
- `ifindis/ifoutdis` - Descartes de entrada/salida

**Índices:** 9 optimizados  
**Constraints:** FK, UNIQUE, CHECK

---

#### 3. **monitoreo.interface_historico**
Series de tiempo para métricas históricas

**Campos clave:**
- `id` (PK) - ID autoincrementable BIGSERIAL
- `devif` (FK) - Interfaz referenciada
- `timestamp` - Momento exacto de la muestra
- Métricas: input, output, ifutil, errores, descartes

**Índices:** 4 para consultas temporales

---

#### 4. **monitoreo.dispositivo_historico**
Series de tiempo para estados de dispositivos

**Campos clave:**
- `id` (PK) - ID autoincrementable BIGSERIAL
- `devid` (FK) - Dispositivo referenciado
- `timestamp` - Momento del evento
- `devstatus` - Estado en ese momento
- `latitud/longitud` - Ubicación en ese momento

**Índices:** 5 para análisis histórico

---

### Funciones y Triggers (6)

#### Funciones Creadas:

1. **`monitoreo.update_timestamp()`**
   - Actualiza automáticamente `updated_at`
   - Trigger en dispositivos e interfaces

2. **`monitoreo.calculate_ifstatus()`**
   - Calcula estado de interfaz automáticamente
   - Lógica: 
     - ifadmin=1 AND ifoper=1 → ifstatus=1 (UP)
     - ifadmin=1 AND ifoper>1 → ifstatus=2 (Down)
     - ifadmin>1 → ifstatus=3 (Shutdown)

3. **`monitoreo.log_dispositivo_estado_change()`**
   - Registra cambios de estado en histórico
   - (Opcional, comentado por defecto)

#### Triggers Activos:

- `trigger_dispositivos_updated_at`
- `trigger_interfaces_updated_at`
- `trigger_calculate_ifstatus`

---

## 🔑 Códigos de Estado

### Estados de Dispositivos (devstatus)

| Código | Nombre | Descripción |
|--------|--------|-------------|
| **0** | No responde | Dispositivo no responde a SNMP |
| **1** | UP | Dispositivo operativo |
| **2** | Caído | Dispositivo fuera de servicio |
| **5** | Fuera de monitoreo | Excluido administrativamente |

### Estados de Interfaces (ifstatus)

| Código | Nombre | Condición | Descripción |
|--------|--------|-----------|-------------|
| **1** | UP | ifadmin=1, ifoper=1 | Interfaz operativa |
| **2** | Down | ifadmin=1, ifoper>1 | Interfaz con falla |
| **3** | Shutdown | ifadmin>1, ifoper>1 | Interfaz apagada |

---

## 📊 Estadísticas del Esquema

### Totales:
```
✓ 1 Esquema creado
✓ 4 Tablas principales
✓ 26+ Índices optimizados
✓ 3 Funciones
✓ 3 Triggers activos
✓ 7 Constraints de integridad
```

### Distribución de Índices:
```
dispositivos            : 8 índices
interfaces              : 9 índices
interface_historico     : 4 índices
dispositivo_historico   : 5 índices
```

---

## 🛠️ Características Avanzadas

### Índices Parciales

Algunos índices solo indexan registros relevantes para mejor rendimiento:

- **`idx_dispositivos_geo`**  
  Solo dispositivos con coordenadas GPS
  
- **`idx_interfaces_errors`**  
  Solo interfaces con errores > 0
  
- **`idx_interfaces_discards`**  
  Solo interfaces con descartes > 0
  
- **`idx_interfaces_ifutil`**  
  Solo interfaces con utilización registrada

### Cascade Delete

Las relaciones están configuradas con `ON DELETE CASCADE`:

```
dispositivos  →  eliminar dispositivo
    ↓
interfaces    →  elimina interfaces del dispositivo
    ↓
interface_historico  →  elimina histórico de las interfaces
```

### Timestamps con Timezone

Todos los campos temporales usan `TIMESTAMP WITH TIME ZONE` para correcta gestión internacional.

---

## ✅ Verificación Post-Instalación

### Script de Verificación Rápida

```sql
-- Verificar esquema
SELECT schema_name 
FROM information_schema.schemata 
WHERE schema_name = 'monitoreo';

-- Verificar tablas
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'monitoreo'
ORDER BY table_name;

-- Resultado esperado:
--  dispositivo_historico
--  dispositivos
--  interface_historico
--  interfaces

-- Verificar triggers
SELECT trigger_name, event_object_table
FROM information_schema.triggers
WHERE trigger_schema = 'monitoreo';

-- Resultado esperado: 3 triggers
```

---

## 📝 Datos de Ejemplo (Opcional)

### Archivo: `07_insert_sample_data.sql`

**Incluye:**
- 10 dispositivos de Claro Chile
- 12 interfaces con diferentes estados
- Distribución geográfica en Chile (Norte, Centro, Sur)

**Casos de prueba:**
✓ Dispositivos UP (7)  
✓ Dispositivo caído (1)  
✓ Dispositivo sin respuesta (1)  
✓ Dispositivo fuera de monitoreo (1)  
✓ Interfaces con alta utilización (95%)  
✓ Interfaces con errores  
✓ Interfaces shutdown  

**⚠️ Importante:** Solo para desarrollo/testing. **NO ejecutar en producción.**

---

## 🔧 Integración con Backend VNM

### Servicios que Usan las Tablas

#### `dispositivos_service.py` usa:
- `monitoreo.dispositivos` - Tabla principal
- `monitoreo.interfaces` - Para conteo de interfaces

**Operaciones:**
- `get_all()` - Listado con filtros
- `get_estadisticas()` - Métricas globales
- `get_with_interfaces_count()` - Dispositivos con contadores
- `buscar()` - Búsqueda general
- `get_valores_filtros()` - Valores únicos para dropdowns

#### `interfaces_service.py` usa:
- `monitoreo.interfaces` - Tabla principal  
- `monitoreo.dispositivos` - Join para datos del dispositivo

**Operaciones:**
- `get_all()` - Listado con filtros
- `get_metricas()` - Métricas globales
- `get_high_utilization()` - Interfaces saturadas
- `get_with_errors()` - Interfaces con problemas
- `get_estadisticas_por_zona()` - Estadísticas por zona

---

## 🐛 Troubleshooting

### Problema: "Permission denied"

```sql
-- Verificar permisos del usuario
GRANT CREATE ON SCHEMA public TO tu_usuario;
GRANT ALL ON SCHEMA monitoreo TO tu_usuario;
```

### Problema: "Schema already exists"

```sql
-- Eliminar esquema existente (CUIDADO: borra datos)
DROP SCHEMA monitoreo CASCADE;
-- Luego ejecutar 00_EJECUTAR_TODOS.sql
```

### Problema: "Relation already exists"

```sql
-- Los scripts usan IF NOT EXISTS
-- Es seguro ejecutar múltiples veces
```

---

## 📚 Recursos Adicionales

### Documentación Relacionada

- **README.md** - Documentación completa (8.2 KB)
- **Modelos SQLAlchemy** - `backend/app/models/`
- **Servicios** - `backend/app/services/`
- **Esquemas Pydantic** - `backend/app/schemas/`

### Archivos del Proyecto

```
vnm-proyectos/
├── backend/
│   ├── app/
│   │   ├── models/
│   │   │   ├── dispositivos.py
│   │   │   └── interfaces.py
│   │   ├── services/
│   │   │   ├── dispositivos_service.py
│   │   │   └── interfaces_service.py
│   │   └── schemas/
│   │       ├── dispositivos.py
│   │       └── interfaces.py
│   └── ...
└── database/  ← ESTAMOS AQUÍ
    ├── 00_EJECUTAR_TODOS.sql
    ├── 01-07 *.sql
    └── README.md
```

---

## 🚀 Próximos Pasos

### 1. Crear Base de Datos
✅ Ejecutar `00_EJECUTAR_TODOS.sql` en PgAdmin

### 2. Verificar Creación
✅ Ejecutar scripts de verificación

### 3. Datos de Prueba (Opcional)
▢ Ejecutar `07_insert_sample_data.sql`

### 4. Configurar Backend
▢ Actualizar `backend/.env` con credenciales DB

### 5. Probar Conexión
▢ Iniciar backend FastAPI
▢ Verificar endpoints de API

### 6. Sincronización
▢ Configurar sincronización con sistema externo (JIPAM)

---

## 👥 Autor

**MiniMax Agent**  
**Proyecto:** VNM - Visual Network Monitoring  
**Fecha:** 2025-10-22  
**Versión:** 1.0.0

---

## ✅ Checklist de Instalación

```
☐ 1. PostgreSQL instalado y funcionando
☐ 2. PgAdmin instalado
☐ 3. Base de datos creada
☐ 4. Conexión a base de datos establecida
☐ 5. Script 00_EJECUTAR_TODOS.sql ejecutado
☐ 6. Verificación de tablas exitosa
☐ 7. Datos de ejemplo insertados (opcional)
☐ 8. Backend configurado con credenciales DB
☐ 9. Prueba de conexión desde backend exitosa
☐ 10. Sistema listo para producción
```

---

**✅ Scripts SQL listos para ejecutar en PgAdmin**
