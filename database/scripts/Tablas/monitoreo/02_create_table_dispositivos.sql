-- ============================================================================
-- VNM - Visual Network Monitoring
-- Tabla: monitoreo.dispositivos
-- Descripción: Catálogo de dispositivos de red monitoreados
-- ============================================================================

-- Eliminar tabla si existe (solo para desarrollo)
-- DROP TABLE IF EXISTS monitoreo.dispositivos CASCADE;

-- Crear tabla dispositivos
CREATE TABLE monitoreo.dispositivos (
    -- Identificación
    devid INTEGER PRIMARY KEY,
    devname VARCHAR(150) NOT NULL,
    devip INET,
    
    -- Ubicación lógica
    operador VARCHAR(50),
    zona VARCHAR(50),
    hub VARCHAR(50),
    area VARCHAR(50),
    
    -- Estado del dispositivo
    devstatus INTEGER NOT NULL DEFAULT 0,
    devstatus_lv TIMESTAMP WITH TIME ZONE,
    devstatus_lc TIMESTAMP WITH TIME ZONE,
    
    -- Información técnica
    enterprise VARCHAR(100),
    modelo VARCHAR(100),
    
    -- Geolocalización
    latitud DECIMAL(10, 8),
    longitud DECIMAL(11, 8),
    
    -- Metadatos
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Comentarios de la tabla y columnas
COMMENT ON TABLE monitoreo.dispositivos IS 'Catálogo de dispositivos de red monitoreados';

COMMENT ON COLUMN monitoreo.dispositivos.devid IS 'ID único del dispositivo (sincronizado con sistema externo)';
COMMENT ON COLUMN monitoreo.dispositivos.devname IS 'Nombre del dispositivo';
COMMENT ON COLUMN monitoreo.dispositivos.devip IS 'Dirección IP del dispositivo';
COMMENT ON COLUMN monitoreo.dispositivos.operador IS 'Operador o compañía propietaria';
COMMENT ON COLUMN monitoreo.dispositivos.zona IS 'Zona geográfica o región';
COMMENT ON COLUMN monitoreo.dispositivos.hub IS 'Hub o nodo central al que pertenece';
COMMENT ON COLUMN monitoreo.dispositivos.area IS 'Área o departamento';
COMMENT ON COLUMN monitoreo.dispositivos.devstatus IS 'Estado del dispositivo: 0=No responde, 1=UP, 2=Caído, 5=Fuera de monitoreo';
COMMENT ON COLUMN monitoreo.dispositivos.devstatus_lv IS 'Last Viewed - Última vez que se vio el dispositivo';
COMMENT ON COLUMN monitoreo.dispositivos.devstatus_lc IS 'Last Changed - Último cambio de estado';
COMMENT ON COLUMN monitoreo.dispositivos.enterprise IS 'Fabricante del dispositivo (Cisco, Huawei, etc.)';
COMMENT ON COLUMN monitoreo.dispositivos.modelo IS 'Modelo del dispositivo';
COMMENT ON COLUMN monitoreo.dispositivos.latitud IS 'Latitud geográfica (coordenadas GPS)';
COMMENT ON COLUMN monitoreo.dispositivos.longitud IS 'Longitud geográfica (coordenadas GPS)';
COMMENT ON COLUMN monitoreo.dispositivos.created_at IS 'Fecha de creación del registro';
COMMENT ON COLUMN monitoreo.dispositivos.updated_at IS 'Fecha de última actualización';

-- Índices para optimización de consultas
CREATE INDEX idx_dispositivos_devstatus ON monitoreo.dispositivos(devstatus);
CREATE INDEX idx_dispositivos_area ON monitoreo.dispositivos(area);
CREATE INDEX idx_dispositivos_hub ON monitoreo.dispositivos(hub);
CREATE INDEX idx_dispositivos_zona ON monitoreo.dispositivos(zona);
CREATE INDEX idx_dispositivos_operador ON monitoreo.dispositivos(operador);
CREATE INDEX idx_dispositivos_enterprise ON monitoreo.dispositivos(enterprise);
CREATE INDEX idx_dispositivos_devname ON monitoreo.dispositivos(devname);
CREATE INDEX idx_dispositivos_geo ON monitoreo.dispositivos(latitud, longitud) WHERE latitud IS NOT NULL AND longitud IS NOT NULL;

-- Comentarios de índices
COMMENT ON INDEX monitoreo.idx_dispositivos_devstatus IS 'Índice para filtros por estado';
COMMENT ON INDEX monitoreo.idx_dispositivos_area IS 'Índice para filtros por área';
COMMENT ON INDEX monitoreo.idx_dispositivos_hub IS 'Índice para filtros por hub';
COMMENT ON INDEX monitoreo.idx_dispositivos_zona IS 'Índice para filtros por zona';
COMMENT ON INDEX monitoreo.idx_dispositivos_operador IS 'Índice para filtros por operador';
COMMENT ON INDEX monitoreo.idx_dispositivos_enterprise IS 'Índice para filtros por fabricante';
COMMENT ON INDEX monitoreo.idx_dispositivos_devname IS 'Índice para búsquedas por nombre';
COMMENT ON INDEX monitoreo.idx_dispositivos_geo IS 'Índice parcial para dispositivos geolocalizados';

-- Verificación
SELECT 
    table_name, 
    column_name, 
    data_type, 
    is_nullable
FROM information_schema.columns
WHERE table_schema = 'monitoreo' 
  AND table_name = 'dispositivos'
ORDER BY ordinal_position;
