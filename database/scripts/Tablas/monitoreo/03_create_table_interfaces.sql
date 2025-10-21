-- ============================================================================
-- VNM - Visual Network Monitoring
-- Tabla: monitoreo.interfaces
-- Descripción: Interfaces de dispositivos con métricas de red
-- ============================================================================

-- Eliminar tabla si existe (solo para desarrollo)
-- DROP TABLE IF EXISTS monitoreo.interfaces CASCADE;

-- Crear tabla interfaces
CREATE TABLE monitoreo.interfaces (
    -- Identificación
    id SERIAL PRIMARY KEY,
    devid INTEGER NOT NULL,
    devif INTEGER NOT NULL,
    
    -- Información de la interfaz
    ifname VARCHAR(100),
    ifalias VARCHAR(255),
    
    -- Estados administrativos y operacionales
    ifadmin INTEGER,
    ifoper INTEGER,
    ifstatus INTEGER,
    
    -- Historial de estados
    iflv TIMESTAMP WITH TIME ZONE,
    iflc TIMESTAMP WITH TIME ZONE,
    
    -- Configuración de monitoreo
    ifgraficar INTEGER DEFAULT 0,
    
    -- Métricas de tráfico
    time TIMESTAMP WITH TIME ZONE,
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
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    -- Constraints
    CONSTRAINT fk_interfaces_dispositivos 
        FOREIGN KEY (devid) 
        REFERENCES monitoreo.dispositivos(devid) 
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    
    CONSTRAINT unique_devid_devif 
        UNIQUE (devid, devif),
    
    CONSTRAINT check_ifstatus 
        CHECK (ifstatus IN (1, 2, 3)),
    
    CONSTRAINT check_ifgraficar 
        CHECK (ifgraficar IN (0, 1)),
    
    CONSTRAINT check_ifutil_range 
        CHECK (ifutil >= 0 AND ifutil <= 100)
);

-- Comentarios de la tabla y columnas
COMMENT ON TABLE monitoreo.interfaces IS 'Interfaces de dispositivos de red con métricas en tiempo real';

COMMENT ON COLUMN monitoreo.interfaces.id IS 'ID autoincrementable único';
COMMENT ON COLUMN monitoreo.interfaces.devid IS 'ID del dispositivo (FK a dispositivos)';
COMMENT ON COLUMN monitoreo.interfaces.devif IS 'ID de interfaz en sistema externo (JIPAM)';
COMMENT ON COLUMN monitoreo.interfaces.ifname IS 'Nombre de la interfaz (ej: GigabitEthernet0/0/1)';
COMMENT ON COLUMN monitoreo.interfaces.ifalias IS 'Alias o descripción de la interfaz';
COMMENT ON COLUMN monitoreo.interfaces.ifadmin IS 'Estado administrativo: 1=Up, >1=Down';
COMMENT ON COLUMN monitoreo.interfaces.ifoper IS 'Estado operacional: 1=Up, >1=Down';
COMMENT ON COLUMN monitoreo.interfaces.ifstatus IS 'Estado consolidado: 1=UP(1,1), 2=Down(1,>1), 3=Shutdown(>1,>1)';
COMMENT ON COLUMN monitoreo.interfaces.iflv IS 'Last Viewed - Última vez que se vio la interfaz';
COMMENT ON COLUMN monitoreo.interfaces.iflc IS 'Last Changed - Último cambio de estado';
COMMENT ON COLUMN monitoreo.interfaces.ifgraficar IS 'Bandera de monitoreo: 0=No monitorear, 1=Monitorear';
COMMENT ON COLUMN monitoreo.interfaces.time IS 'Timestamp de la última muestra de métricas';
COMMENT ON COLUMN monitoreo.interfaces.input IS 'Data rate de entrada en bps (bits por segundo)';
COMMENT ON COLUMN monitoreo.interfaces.output IS 'Data rate de salida en bps (bits por segundo)';
COMMENT ON COLUMN monitoreo.interfaces.ifspeed IS 'Velocidad del enlace en Mbps';
COMMENT ON COLUMN monitoreo.interfaces.ifindis IS 'Tasa de descartes de entrada (paquetes/segundo)';
COMMENT ON COLUMN monitoreo.interfaces.ifoutdis IS 'Tasa de descartes de salida (paquetes/segundo)';
COMMENT ON COLUMN monitoreo.interfaces.ifinerr IS 'Tasa de errores de entrada (paquetes/segundo)';
COMMENT ON COLUMN monitoreo.interfaces.ifouterr IS 'Tasa de errores de salida (paquetes/segundo)';
COMMENT ON COLUMN monitoreo.interfaces.ifutil IS 'Porcentaje de utilización del enlace (0-100%)';
COMMENT ON COLUMN monitoreo.interfaces.created_at IS 'Fecha de creación del registro';
COMMENT ON COLUMN monitoreo.interfaces.updated_at IS 'Fecha de última actualización';

-- Índices para optimización de consultas
CREATE INDEX idx_interfaces_devid ON monitoreo.interfaces(devid);
CREATE INDEX idx_interfaces_devif ON monitoreo.interfaces(devif);
CREATE INDEX idx_interfaces_ifstatus ON monitoreo.interfaces(ifstatus);
CREATE INDEX idx_interfaces_ifgraficar ON monitoreo.interfaces(ifgraficar);
CREATE INDEX idx_interfaces_ifutil ON monitoreo.interfaces(ifutil) WHERE ifutil IS NOT NULL;
CREATE INDEX idx_interfaces_ifspeed ON monitoreo.interfaces(ifspeed) WHERE ifspeed IS NOT NULL;
CREATE INDEX idx_interfaces_errors ON monitoreo.interfaces(ifinerr, ifouterr) WHERE (ifinerr > 0 OR ifouterr > 0);
CREATE INDEX idx_interfaces_discards ON monitoreo.interfaces(ifindis, ifoutdis) WHERE (ifindis > 0 OR ifoutdis > 0);
CREATE INDEX idx_interfaces_time ON monitoreo.interfaces(time DESC);

-- Comentarios de índices
COMMENT ON INDEX monitoreo.idx_interfaces_devid IS 'Índice para joins con dispositivos';
COMMENT ON INDEX monitoreo.idx_interfaces_devif IS 'Índice para búsquedas por devif';
COMMENT ON INDEX monitoreo.idx_interfaces_ifstatus IS 'Índice para filtros por estado';
COMMENT ON INDEX monitoreo.idx_interfaces_ifgraficar IS 'Índice para filtros por interfaces monitoreadas';
COMMENT ON INDEX monitoreo.idx_interfaces_ifutil IS 'Índice parcial para búsquedas por utilización';
COMMENT ON INDEX monitoreo.idx_interfaces_ifspeed IS 'Índice parcial para búsquedas por velocidad';
COMMENT ON INDEX monitoreo.idx_interfaces_errors IS 'Índice parcial para interfaces con errores';
COMMENT ON INDEX monitoreo.idx_interfaces_discards IS 'Índice parcial para interfaces con descartes';
COMMENT ON INDEX monitoreo.idx_interfaces_time IS 'Índice para ordenar por timestamp descendente';

-- Verificación
SELECT 
    table_name, 
    column_name, 
    data_type, 
    is_nullable
FROM information_schema.columns
WHERE table_schema = 'monitoreo' 
  AND table_name = 'interfaces'
ORDER BY ordinal_position;
