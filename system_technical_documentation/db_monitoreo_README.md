# Scripts de Base de Datos - VNM

## 📊 Esquema de Monitoreo de Red

Este directorio contiene todos los scripts SQL necesarios para crear el esquema de base de datos del sistema VNM (Visual Network Monitoring).

---

## 📁 Estructura de Archivos

### Scripts de Creación (Orden de Ejecución)

```
database/
├── 00_EJECUTAR_TODOS.sql          ← 🚀 SCRIPT MAESTRO (ejecutar este)
├── 01_create_schema_monitoreo.sql
├── 02_create_table_dispositivos.sql
├── 03_create_table_interfaces.sql
├── 04_create_table_interface_historico.sql
├── 05_create_table_dispositivo_historico.sql
├── 06_create_triggers_and_functions.sql
├── 07_insert_sample_data.sql       ← OPCIONAL (datos de prueba)
└── README.md
```

---

## 🚀 Inicio Rápido

### Opción 1: Ejecutar Script Maestro (Recomendado)

1. Abrir **PgAdmin**
2. Conectarse a tu base de datos PostgreSQL
3. Abrir el **Query Tool** (Tools > Query Tool)
4. Cargar el archivo: `00_EJECUTAR_TODOS.sql`
5. Ejecutar (F5 o botón Execute)

```sql
-- Esto creará automáticamente:
-- ✓ Esquema monitoreo
-- ✓ 4 tablas principales
-- ✓ 26+ índices optimizados
-- ✓ 3 funciones
-- ✓ 3 triggers
```

### Opción 2: Ejecutar Scripts Individuales

Si prefieres ejecutar paso a paso:

```bash
01 → Crear esquema
02 → Tabla dispositivos
03 → Tabla interfaces
04 → Tabla interface_historico
05 → Tabla dispositivo_historico
06 → Funciones y triggers
07 → Datos de ejemplo (opcional)
```

---

## 📋 Descripción de Scripts

### `00_EJECUTAR_TODOS.sql` 🚀
**Script maestro que crea todo el esquema completo.**

- Ejecuta todos los pasos en orden
- Incluye mensajes de progreso
- Muestra resumen al final
- Uso recomendado para instalaciones nuevas

---

### `01_create_schema_monitoreo.sql`
**Crea el esquema `monitoreo`.**

```sql
CREATE SCHEMA monitoreo;
```

- Esquema separado para datos de red
- Solo lectura desde sistema externo
- Aislado de otros esquemas

---

### `02_create_table_dispositivos.sql`
**Tabla principal de dispositivos de red.**

**Campos principales:**
- `devid` - ID único del dispositivo
- `devname` - Nombre del dispositivo
- `devip` - Dirección IP
- `devstatus` - Estado (0=No responde, 1=UP, 2=Caído, 5=Fuera)
- `enterprise` - Fabricante (Cisco, Huawei, etc.)
- `latitud/longitud` - Geolocalización

**Índices creados:** 8

---

### `03_create_table_interfaces.sql`
**Tabla de interfaces con métricas de red.**

**Campos principales:**
- `devid` - Referencia al dispositivo
- `devif` - ID de interfaz
- `ifstatus` - Estado (1=UP, 2=Down, 3=Shutdown)
- `input/output` - Tráfico en bps
- `ifutil` - Utilización en %
- `ifinerr/ifouterr` - Errores
- `ifindis/ifoutdis` - Descartes

**Índices creados:** 9

**Constraints:**
- Foreign Key a dispositivos
- Unique (devid, devif)
- Check ifstatus IN (1,2,3)
- Check ifutil 0-100%

---

### `04_create_table_interface_historico.sql`
**Series de tiempo para métricas históricas de interfaces.**

- Almacena snapshots de métricas
- Optimizada para consultas temporales
- Índices para agregaciones por hora

**Índices creados:** 4

---

### `05_create_table_dispositivo_historico.sql`
**Series de tiempo para estados de dispositivos.**

- Registra cambios de estado
- Tracking de disponibilidad
- Índices para agregaciones por día

**Índices creados:** 5

---

### `06_create_triggers_and_functions.sql`
**Automatizaciones y lógica de negocio.**

**Funciones creadas:**

1. **`update_timestamp()`**
   - Actualiza `updated_at` automáticamente

2. **`calculate_ifstatus()`**
   - Calcula estado de interfaz desde ifadmin/ifoper
   - Lógica: UP(1,1), Down(1,>1), Shutdown(>1,>1)

3. **`log_dispositivo_estado_change()`**
   - Registra cambios de estado en histórico
   - (Trigger opcional, comentado por defecto)

**Triggers activos:**
- `trigger_dispositivos_updated_at` - Auto-update timestamp
- `trigger_interfaces_updated_at` - Auto-update timestamp
- `trigger_calculate_ifstatus` - Auto-calcular estado interfaz

---

### `07_insert_sample_data.sql` (OPCIONAL)
**Datos de ejemplo para testing.**

**Incluye:**
- 10 dispositivos de ejemplo (Claro Chile)
- Distribuidos en zonas Norte, Centro, Sur
- 12 interfaces con diferentes estados
- Casos de prueba:
  - Dispositivos UP
  - Dispositivo caído
  - Dispositivo sin respuesta
  - Interfaces con alta utilización
  - Interfaces con errores
  - Interfaces shutdown

**⚠️ Nota:** Solo para desarrollo/testing. NO ejecutar en producción.

---

## 📊 Estructura de Datos Creada

```
monitoreo (esquema)
├── dispositivos
│   ├── PK: devid
│   └── 8 índices
│
├── interfaces
│   ├── PK: id
│   ├── FK: devid → dispositivos.devid
│   ├── UNIQUE: (devid, devif)
│   └── 9 índices
│
├── interface_historico
│   ├── PK: id
│   ├── FK: devif → interfaces.devif
│   └── 4 índices
│
└── dispositivo_historico
    ├── PK: id
    ├── FK: devid → dispositivos.devid
    └── 5 índices
```

**Total:**
- 4 tablas
- 26+ índices optimizados
- 3 funciones
- 3 triggers
- 7 constraints

---

## 🔑 Códigos de Estado

### Estados de Dispositivos (`devstatus`)

| Código | Estado | Descripción |
|--------|--------|-------------|
| 0 | No responde | Dispositivo no responde a SNMP |
| 1 | UP | Dispositivo operativo |
| 2 | Caído | Dispositivo fuera de servicio |
| 5 | Fuera de monitoreo | Excluido administrativamente |

### Estados de Interfaces (`ifstatus`)

| Código | Estado | ifadmin | ifoper | Descripción |
|--------|--------|---------|--------|-------------|
| 1 | UP | 1 | 1 | Interfaz operativa |
| 2 | Down | 1 | >1 | Interfaz con falla |
| 3 | Shutdown | >1 | >1 | Interfaz apagada |

---

## ⚙️ Requisitos

- **PostgreSQL** 12 o superior
- **Permisos:** CREATE SCHEMA, CREATE TABLE, CREATE INDEX, CREATE FUNCTION, CREATE TRIGGER
- **Cliente:** PgAdmin 4 (recomendado) o psql

---

## ✅ Verificación Post-Instalación

### Verificar esquema creado:
```sql
SELECT schema_name 
FROM information_schema.schemata 
WHERE schema_name = 'monitoreo';
```

### Verificar tablas:
```sql
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'monitoreo'
ORDER BY table_name;
```

### Verificar índices:
```sql
SELECT 
    tablename, 
    indexname 
FROM pg_indexes 
WHERE schemaname = 'monitoreo'
ORDER BY tablename, indexname;
```

### Verificar triggers:
```sql
SELECT 
    trigger_name,
    event_object_table,
    action_timing,
    event_manipulation
FROM information_schema.triggers
WHERE trigger_schema = 'monitoreo'
ORDER BY event_object_table, trigger_name;
```

---

## 🛠️ Mantenimiento

### Limpiar tablas (mantener estructura):
```sql
TRUNCATE TABLE monitoreo.interface_historico CASCADE;
TRUNCATE TABLE monitoreo.dispositivo_historico CASCADE;
TRUNCATE TABLE monitoreo.interfaces CASCADE;
TRUNCATE TABLE monitoreo.dispositivos CASCADE;
```

### Eliminar esquema completo:
```sql
DROP SCHEMA monitoreo CASCADE;
```

### Recrear desde cero:
```sql
DROP SCHEMA IF EXISTS monitoreo CASCADE;
-- Luego ejecutar 00_EJECUTAR_TODOS.sql
```

---

## 📝 Notas Importantes

1. **Orden de Ejecución:** Los scripts deben ejecutarse en orden numérico (01, 02, 03...)

2. **Foreign Keys:** Las relaciones CASCADE están configuradas:
   - Eliminar dispositivo → elimina sus interfaces
   - Eliminar interfaz → elimina su histórico

3. **Índices Parciales:** Algunos índices solo indexan registros relevantes:
   - `idx_dispositivos_geo` - Solo dispositivos con coordenadas
   - `idx_interfaces_errors` - Solo interfaces con errores
   - `idx_interfaces_discards` - Solo interfaces con descartes

4. **Timestamps:** Todos usan `TIMESTAMP WITH TIME ZONE` para correcta gestión de husos horarios

5. **Auto-increment:** 
   - `interfaces.id` usa SERIAL
   - Tablas históricas usan BIGSERIAL (soporte para millones de registros)

---

## 👥 Autor

**MiniMax Agent**  
Proyecto: VNM - Visual Network Monitoring  
Fecha: 2025-10-22

---

## 📞 Soporte

Para problemas o consultas sobre los scripts SQL:

1. Verificar logs de PostgreSQL
2. Revisar permisos de usuario
3. Comprobar versión de PostgreSQL
4. Consultar documentación del proyecto VNM

---

**✅ Scripts listos para producción**
