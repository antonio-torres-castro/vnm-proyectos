-- ============================================================================
-- VNM - Visual Network Monitoring
-- Tabla: monitoreo.dispositivo_historico
-- Descripción: Series de tiempo para estados históricos de dispositivos
-- ============================================================================

-- Eliminar tabla si existe (solo para desarrollo)
-- DROP TABLE IF EXISTS monitoreo.dispositivo_historico CASCADE;

-- Crear tabla dispositivo_historico
CREATE TABLE monitoreo.dispositivo_historico (
    -- Identificación
    id BIGSERIAL PRIMARY KEY,
    devid INTEGER NOT NULL,
    timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
    
    -- Estado del dispositivo
    devstatus INTEGER NOT NULL,
    
    -- Geolocalización (puede cambiar en el tiempo)
    latitud DECIMAL(10, 8),
    longitud DECIMAL(11, 8),
    
    -- Metadatos
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    -- Constraints
    CONSTRAINT fk_dispositivo_historico_dispositivos 
        FOREIGN KEY (devid) 
        REFERENCES monitoreo.dispositivos(devid) 
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    
    CONSTRAINT check_historico_devstatus 
        CHECK (devstatus IN (0, 1, 2, 5))
);

-- Comentarios de la tabla y columnas
COMMENT ON TABLE monitoreo.dispositivo_historico IS 'Histórico de estados de dispositivos (series de tiempo)';

COMMENT ON COLUMN monitoreo.dispositivo_historico.id IS 'ID autoincrementable único';
COMMENT ON COLUMN monitoreo.dispositivo_historico.devid IS 'ID del dispositivo (FK a dispositivos)';
COMMENT ON COLUMN monitoreo.dispositivo_historico.timestamp IS 'Momento exacto del evento';
COMMENT ON COLUMN monitoreo.dispositivo_historico.devstatus IS 'Estado: 0=No responde, 1=UP, 2=Caído, 5=Fuera de monitoreo';
COMMENT ON COLUMN monitoreo.dispositivo_historico.latitud IS 'Latitud al momento del evento';
COMMENT ON COLUMN monitoreo.dispositivo_historico.longitud IS 'Longitud al momento del evento';
COMMENT ON COLUMN monitoreo.dispositivo_historico.created_at IS 'Fecha de inserción del registro';

-- Índices para optimización de consultas de series de tiempo
CREATE INDEX idx_dispositivo_historico_devid ON monitoreo.dispositivo_historico(devid);
CREATE INDEX idx_dispositivo_historico_timestamp ON monitoreo.dispositivo_historico(timestamp DESC);
CREATE INDEX idx_dispositivo_historico_devid_timestamp ON monitoreo.dispositivo_historico(devid, timestamp DESC);
CREATE INDEX idx_dispositivo_historico_devstatus ON monitoreo.dispositivo_historico(devstatus);

-- Comentarios de índices
COMMENT ON INDEX monitoreo.idx_dispositivo_historico_devid IS 'Índice para consultas por dispositivo';
COMMENT ON INDEX monitoreo.idx_dispositivo_historico_timestamp IS 'Índice para consultas por rango temporal';
COMMENT ON INDEX monitoreo.idx_dispositivo_historico_devid_timestamp IS 'Índice compuesto para consultas históricas por dispositivo';
COMMENT ON INDEX monitoreo.idx_dispositivo_historico_devstatus IS 'Índice para análisis de estados';

-- Verificación
SELECT 
    table_name, 
    column_name, 
    data_type, 
    is_nullable
FROM information_schema.columns
WHERE table_schema = 'monitoreo' 
  AND table_name = 'dispositivo_historico'
ORDER BY ordinal_position;
