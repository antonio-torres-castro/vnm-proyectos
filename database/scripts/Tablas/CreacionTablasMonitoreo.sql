-- ==========================================
-- SCRIPT DE CREACIÓN DE TABLAS MONITOREO - PostgreSQL 16.4
-- Sistema de Monitoreo de Red VNM
-- ==========================================

-- Configuración inicial
CREATE SCHEMA IF NOT EXISTS monitoreo AUTHORIZATION CURRENT_USER;

SET search_path TO monitoreo;

-- ==========================================
-- TABLA: dispositivos (Catálogo de dispositivos de red)
-- ==========================================
CREATE TABLE dispositivos (
    devid INTEGER PRIMARY KEY,
    operador VARCHAR(50),
    zona VARCHAR(50),
    hub VARCHAR(50),
    devip INET,
    area VARCHAR(50),
    devname VARCHAR(150),
    devstatus INTEGER,                    -- 0:No responde, 1:UP, 2:Caído, 5:Fuera de monitoreo
    devstatus_lv TIMESTAMP WITH TIME ZONE, -- Última vez que se vio
    devstatus_lc TIMESTAMP WITH TIME ZONE, -- Último cambio de estado
    enterprise VARCHAR(100),              -- Fabricante
    modelo VARCHAR(100),
    latitud DECIMAL(10,8),
    longitud DECIMAL(11,8),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- ==========================================
-- TABLA: interfaces (Interfaces de dispositivos con métricas)
-- ==========================================
CREATE TABLE interfaces (
    id SERIAL PRIMARY KEY,
    devid INTEGER NOT NULL,
    devif INTEGER NOT NULL,               -- ID de interface en JIPAM
    ifname VARCHAR(100),
    ifalias VARCHAR(255),
    ifadmin INTEGER,                      -- 1:Up, >1:Down
    ifoper INTEGER,                       -- 1:Up, >1:Down
    ifstatus INTEGER,                     -- 1:UP(1,1), 2:Down(1,>1), 3:Shutdown(2,>1)
    iflv TIMESTAMP WITH TIME ZONE,        -- Última vez que se vio
    iflc TIMESTAMP WITH TIME ZONE,        -- Último cambio de estado
    ifgraficar INTEGER,                   -- 0:No monitoreo, 1:En monitoreo
    time TIMESTAMP WITH TIME ZONE,        -- Fecha/hora última muestra
    input BIGINT,                         -- Data rate entrada (bps)
    output BIGINT,                        -- Data rate salida (bps)
    ifspeed INTEGER,                      -- Link Speed (Mbps)
    ifindis INTEGER,                      -- Descartes entrada (rate/s)
    ifoutdis INTEGER,                     -- Descartes salida (rate/s)
    ifinerr INTEGER,                      -- Errores entrada (rate/s)
    ifouterr INTEGER,                     -- Errores salida (rate/s)
    ifutil DECIMAL(5,2),                  -- Utilización (%)
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    
    FOREIGN KEY (devid) REFERENCES dispositivos(devid) ON DELETE CASCADE
);

-- ==========================================
-- TABLA: interface_historico (Series de tiempo para métricas)
-- ==========================================
CREATE TABLE interface_historico (
    id SERIAL PRIMARY KEY,
    devif INTEGER NOT NULL,
    timestamp TIMESTAMP WITH TIME ZONE,
    input BIGINT,                         -- Data rate entrada (bps)
    output BIGINT,                        -- Data rate salida (bps)
    ifspeed INTEGER,                      -- Link Speed (Mbps)
    ifindis INTEGER,                      -- Descartes entrada (rate/s)
    ifoutdis INTEGER,                     -- Descartes salida (rate/s)
    ifinerr INTEGER,                      -- Errores entrada (rate/s)
    ifouterr INTEGER,                     -- Errores salida (rate/s)
    ifutil DECIMAL(5,2),                  -- Utilización (%)
    created_at TIMESTAMP DEFAULT NOW(),
    
    FOREIGN KEY (devif) REFERENCES interfaces(devif) ON DELETE CASCADE
);

-- ==========================================
-- TABLA: dispositivo_historico (Series de tiempo para estado de dispositivos)
-- ==========================================
CREATE TABLE dispositivo_historico (
    id SERIAL PRIMARY KEY,
    devid INTEGER NOT NULL,
    timestamp TIMESTAMP WITH TIME ZONE,
    devstatus INTEGER,
    latitud DECIMAL(10,8),
    longitud DECIMAL(11,8),
    created_at TIMESTAMP DEFAULT NOW(),
    
    FOREIGN KEY (devid) REFERENCES dispositivos(devid) ON DELETE CASCADE
);

-- ==========================================
-- ÍNDICES PARA OPTIMIZACIÓN
-- ==========================================

-- Índices para tabla dispositivos
CREATE INDEX idx_dispositivos_devstatus ON dispositivos(devstatus);
CREATE INDEX idx_dispositivos_area ON dispositivos(area);
CREATE INDEX idx_dispositivos_hub ON dispositivos(hub);
CREATE INDEX idx_dispositivos_enterprise ON dispositivos(enterprise);

-- Índices para tabla interfaces
CREATE INDEX idx_interfaces_devid ON interfaces(devid);
CREATE INDEX idx_interfaces_ifstatus ON interfaces(ifstatus);
CREATE INDEX idx_interfaces_ifgraficar ON interfaces(ifgraficar);
CREATE UNIQUE INDEX idx_interfaces_devif_unique ON interfaces(devid, devif);

-- Índices para tabla interface_historico (optimización de consultas históricas)
CREATE INDEX idx_interface_historico_devif ON interface_historico(devif);
CREATE INDEX idx_interface_historico_timestamp ON interface_historico(timestamp);
CREATE INDEX idx_interface_historico_devif_timestamp ON interface_historico(devif, timestamp);

-- Índices para tabla dispositivo_historico
CREATE INDEX idx_dispositivo_historico_devid ON dispositivo_historico(devid);
CREATE INDEX idx_dispositivo_historico_timestamp ON dispositivo_historico(timestamp);

-- ==========================================
-- COMENTARIOS PARA DOCUMENTACIÓN
-- ==========================================
COMMENT ON SCHEMA monitoreo IS 'Esquema de monitoreo de red VNM (solo lectura para visualización)';

COMMENT ON TABLE dispositivos IS 'Catálogo maestro de dispositivos de red monitoreados';
COMMENT ON COLUMN dispositivos.devstatus IS '0:No responde, 1:UP, 2:Caído, 5:Fuera de monitoreo';
COMMENT ON COLUMN dispositivos.devstatus_lv IS 'Timestamp de última vez que se vio el dispositivo';
COMMENT ON COLUMN dispositivos.devstatus_lc IS 'Timestamp de último cambio de estado';

COMMENT ON TABLE interfaces IS 'Interfaces de dispositivos con métricas de red actuales';
COMMENT ON COLUMN interfaces.ifstatus IS '1:UP(1,1), 2:Down(1,>1), 3:Shutdown(2,>1)';
COMMENT ON COLUMN interfaces.ifgraficar IS '0:No monitoreo, 1:En monitoreo';
COMMENT ON COLUMN interfaces.input IS 'Data rate entrada en bits por segundo (bps)';
COMMENT ON COLUMN interfaces.output IS 'Data rate salida en bits por segundo (bps)';
COMMENT ON COLUMN interfaces.ifutil IS 'Porcentaje de utilización de la interface';

COMMENT ON TABLE interface_historico IS 'Series temporales de métricas de interfaces para análisis histórico';

COMMENT ON TABLE dispositivo_historico IS 'Series temporales de estados de dispositivos para análisis histórico';

-- ==========================================
-- MENSAJE DE CONFIRMACIÓN
-- ==========================================
SELECT 'Esquema de monitoreo creado correctamente' as status;
