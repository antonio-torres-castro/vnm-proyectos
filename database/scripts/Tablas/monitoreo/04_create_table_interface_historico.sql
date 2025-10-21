-- ============================================================================
-- VNM - Visual Network Monitoring
-- Tabla: monitoreo.interface_historico
-- Descripción: Series de tiempo para métricas históricas de interfaces
-- ============================================================================

-- Eliminar tabla si existe (solo para desarrollo)
-- DROP TABLE IF EXISTS monitoreo.interface_historico CASCADE;

-- Crear tabla interface_historico
CREATE TABLE monitoreo.interface_historico (
    -- Identificación
    id BIGSERIAL PRIMARY KEY,
    devid INTEGER NOT NULL,
    devif INTEGER NOT NULL,
    timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
    
    -- Métricas de tráfico
    input BIGINT,
    output BIGINT,
    ifspeed INTEGER,
    
    -- Métricas de errores y descartes
    ifindis INTEGER,
    ifoutdis INTEGER,
    ifinerr INTEGER,
    ifouterr INTEGER,
    
    -- Métricas calculadas
    ifutil DECIMAL(5, 2),
    
    -- Metadatos
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    -- Constraints
    CONSTRAINT fk_interface_historico_interfaces 
        FOREIGN KEY (devid, devif) 
        REFERENCES monitoreo.interfaces(devid, devif) 
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    
    CONSTRAINT check_historico_ifutil_range 
        CHECK (ifutil >= 0 AND ifutil <= 100)
);

-- Comentarios de la tabla y columnas
COMMENT ON TABLE monitoreo.interface_historico IS 'Histórico de métricas de interfaces (series de tiempo)';

COMMENT ON COLUMN monitoreo.interface_historico.id IS 'ID autoincrementable único';
COMMENT ON COLUMN monitoreo.interface_historico.devid IS 'ID del dispositivo (FK compuesta)';
COMMENT ON COLUMN monitoreo.interface_historico.devif IS 'ID de la interfaz (FK compuesta a interfaces.devid+devif)';
COMMENT ON COLUMN monitoreo.interface_historico.timestamp IS 'Momento exacto de la muestra';
COMMENT ON COLUMN monitoreo.interface_historico.input IS 'Data rate de entrada en bps';
COMMENT ON COLUMN monitoreo.interface_historico.output IS 'Data rate de salida en bps';
COMMENT ON COLUMN monitoreo.interface_historico.ifspeed IS 'Velocidad del enlace en Mbps';
COMMENT ON COLUMN monitoreo.interface_historico.ifindis IS 'Tasa de descartes de entrada';
COMMENT ON COLUMN monitoreo.interface_historico.ifoutdis IS 'Tasa de descartes de salida';
COMMENT ON COLUMN monitoreo.interface_historico.ifinerr IS 'Tasa de errores de entrada';
COMMENT ON COLUMN monitoreo.interface_historico.ifouterr IS 'Tasa de errores de salida';
COMMENT ON COLUMN monitoreo.interface_historico.ifutil IS 'Porcentaje de utilización (0-100%)';
COMMENT ON COLUMN monitoreo.interface_historico.created_at IS 'Fecha de inserción del registro';

-- Índices para optimización de consultas de series de tiempo
CREATE INDEX idx_interface_historico_devid ON monitoreo.interface_historico(devid);
CREATE INDEX idx_interface_historico_devif ON monitoreo.interface_historico(devif);
CREATE INDEX idx_interface_historico_timestamp ON monitoreo.interface_historico(timestamp DESC);
CREATE INDEX idx_interface_historico_devid_devif_timestamp ON monitoreo.interface_historico(devid, devif, timestamp DESC);

-- Comentarios de índices
COMMENT ON INDEX monitoreo.idx_interface_historico_devid IS 'Índice para consultas por dispositivo';
COMMENT ON INDEX monitoreo.idx_interface_historico_devif IS 'Índice para consultas por interfaz';
COMMENT ON INDEX monitoreo.idx_interface_historico_timestamp IS 'Índice para consultas por rango temporal';
COMMENT ON INDEX monitoreo.idx_interface_historico_devid_devif_timestamp IS 'Índice compuesto para consultas históricas por interfaz';

-- Verificación
SELECT 
    table_name, 
    column_name, 
    data_type, 
    is_nullable
FROM information_schema.columns
WHERE table_schema = 'monitoreo' 
  AND table_name = 'interface_historico'
ORDER BY ordinal_position;
