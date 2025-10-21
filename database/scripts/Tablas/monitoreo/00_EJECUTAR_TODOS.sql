-- ============================================================================
-- VNM - Visual Network Monitoring
-- Script Maestro de Creación de Base de Datos
-- Ejecutar este archivo para crear todo el esquema de monitoreo
-- ============================================================================
--
-- INSTRUCCIONES:
-- 1. Conectarse a la base de datos PostgreSQL con PgAdmin
-- 2. Abrir este archivo en el Query Tool
-- 3. Ejecutar todo el script (F5 o botón Execute)
--
-- NOTA: Los scripts individuales también pueden ejecutarse por separado
-- en el orden indicado (01, 02, 03, etc.)
-- ============================================================================

DO $$
BEGIN
    RAISE NOTICE '';
    RAISE NOTICE '============================================================================';
    RAISE NOTICE 'VNM - Visual Network Monitoring';
    RAISE NOTICE 'Creación del Esquema de Monitoreo';
    RAISE NOTICE '============================================================================';
    RAISE NOTICE '';
END $$;

-- ============================================================================
-- PASO 1: Crear el esquema
-- ============================================================================
DO $$
BEGIN
    RAISE NOTICE 'PASO 1/7: Creando esquema monitoreo...';
END $$;

DROP SCHEMA IF EXISTS monitoreo CASCADE;
CREATE SCHEMA monitoreo;
COMMENT ON SCHEMA monitoreo IS 'Esquema para datos de monitoreo de red - Solo lectura desde sistema externo';

DO $$
BEGIN
    RAISE NOTICE '  ✓ Esquema creado exitosamente';
    RAISE NOTICE '';
END $$;

-- ============================================================================
-- PASO 2: Crear tabla dispositivos
-- ============================================================================
DO $$
BEGIN
    RAISE NOTICE 'PASO 2/7: Creando tabla dispositivos...';
END $$;

CREATE TABLE monitoreo.dispositivos (
    devid INTEGER PRIMARY KEY,
    devname VARCHAR(150) NOT NULL,
    devip INET,
    operador VARCHAR(50),
    zona VARCHAR(50),
    hub VARCHAR(50),
    area VARCHAR(50),
    devstatus INTEGER NOT NULL DEFAULT 0,
    devstatus_lv TIMESTAMP WITH TIME ZONE,
    devstatus_lc TIMESTAMP WITH TIME ZONE,
    enterprise VARCHAR(100),
    modelo VARCHAR(100),
    latitud DECIMAL(10, 8),
    longitud DECIMAL(11, 8),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

COMMENT ON TABLE monitoreo.dispositivos IS 'Catálogo de dispositivos de red monitoreados';

CREATE INDEX idx_dispositivos_devstatus ON monitoreo.dispositivos(devstatus);
CREATE INDEX idx_dispositivos_area ON monitoreo.dispositivos(area);
CREATE INDEX idx_dispositivos_hub ON monitoreo.dispositivos(hub);
CREATE INDEX idx_dispositivos_zona ON monitoreo.dispositivos(zona);
CREATE INDEX idx_dispositivos_operador ON monitoreo.dispositivos(operador);
CREATE INDEX idx_dispositivos_enterprise ON monitoreo.dispositivos(enterprise);
CREATE INDEX idx_dispositivos_devname ON monitoreo.dispositivos(devname);
CREATE INDEX idx_dispositivos_geo ON monitoreo.dispositivos(latitud, longitud) WHERE latitud IS NOT NULL AND longitud IS NOT NULL;

DO $$
BEGIN
    RAISE NOTICE '  ✓ Tabla dispositivos creada con 8 índices';
    RAISE NOTICE '';
END $$;

-- ============================================================================
-- PASO 3: Crear tabla interfaces
-- ============================================================================
DO $$
BEGIN
    RAISE NOTICE 'PASO 3/7: Creando tabla interfaces...';
END $$;

CREATE TABLE monitoreo.interfaces (
    id SERIAL PRIMARY KEY,
    devid INTEGER NOT NULL,
    devif INTEGER NOT NULL,
    ifname VARCHAR(100),
    ifalias VARCHAR(255),
    ifadmin INTEGER,
    ifoper INTEGER,
    ifstatus INTEGER,
    iflv TIMESTAMP WITH TIME ZONE,
    iflc TIMESTAMP WITH TIME ZONE,
    ifgraficar INTEGER DEFAULT 0,
    time TIMESTAMP WITH TIME ZONE,
    input BIGINT,
    output BIGINT,
    ifspeed INTEGER,
    ifindis INTEGER,
    ifoutdis INTEGER,
    ifinerr INTEGER,
    ifouterr INTEGER,
    ifutil DECIMAL(5, 2),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
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

COMMENT ON TABLE monitoreo.interfaces IS 'Interfaces de dispositivos de red con métricas en tiempo real';

CREATE INDEX idx_interfaces_devid ON monitoreo.interfaces(devid);
CREATE INDEX idx_interfaces_devif ON monitoreo.interfaces(devif);
CREATE INDEX idx_interfaces_ifstatus ON monitoreo.interfaces(ifstatus);
CREATE INDEX idx_interfaces_ifgraficar ON monitoreo.interfaces(ifgraficar);
CREATE INDEX idx_interfaces_ifutil ON monitoreo.interfaces(ifutil) WHERE ifutil IS NOT NULL;
CREATE INDEX idx_interfaces_ifspeed ON monitoreo.interfaces(ifspeed) WHERE ifspeed IS NOT NULL;
CREATE INDEX idx_interfaces_errors ON monitoreo.interfaces(ifinerr, ifouterr) WHERE (ifinerr > 0 OR ifouterr > 0);
CREATE INDEX idx_interfaces_discards ON monitoreo.interfaces(ifindis, ifoutdis) WHERE (ifindis > 0 OR ifoutdis > 0);
CREATE INDEX idx_interfaces_time ON monitoreo.interfaces(time DESC);

DO $$
BEGIN
    RAISE NOTICE '  ✓ Tabla interfaces creada con 9 índices';
    RAISE NOTICE '';
END $$;

-- ============================================================================
-- PASO 4: Crear tabla interface_historico
-- ============================================================================
DO $$
BEGIN
    RAISE NOTICE 'PASO 4/7: Creando tabla interface_historico...';
END $$;

CREATE TABLE monitoreo.interface_historico (
    id BIGSERIAL PRIMARY KEY,
    devid INTEGER NOT NULL,
    devif INTEGER NOT NULL,
    timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
    input BIGINT,
    output BIGINT,
    ifspeed INTEGER,
    ifindis INTEGER,
    ifoutdis INTEGER,
    ifinerr INTEGER,
    ifouterr INTEGER,
    ifutil DECIMAL(5, 2),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    CONSTRAINT fk_interface_historico_interfaces 
        FOREIGN KEY (devid, devif) 
        REFERENCES monitoreo.interfaces(devid, devif) 
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    CONSTRAINT check_historico_ifutil_range 
        CHECK (ifutil >= 0 AND ifutil <= 100)
);

COMMENT ON TABLE monitoreo.interface_historico IS 'Histórico de métricas de interfaces (series de tiempo)';

CREATE INDEX idx_interface_historico_devid ON monitoreo.interface_historico(devid);
CREATE INDEX idx_interface_historico_devif ON monitoreo.interface_historico(devif);
CREATE INDEX idx_interface_historico_timestamp ON monitoreo.interface_historico(timestamp DESC);
CREATE INDEX idx_interface_historico_devid_devif_timestamp ON monitoreo.interface_historico(devid, devif, timestamp DESC);

DO $$
BEGIN
    RAISE NOTICE '  ✓ Tabla interface_historico creada con 4 índices';
    RAISE NOTICE '';
END $$;

-- ============================================================================
-- PASO 5: Crear tabla dispositivo_historico
-- ============================================================================
DO $$
BEGIN
    RAISE NOTICE 'PASO 5/7: Creando tabla dispositivo_historico...';
END $$;

CREATE TABLE monitoreo.dispositivo_historico (
    id BIGSERIAL PRIMARY KEY,
    devid INTEGER NOT NULL,
    timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
    devstatus INTEGER NOT NULL,
    latitud DECIMAL(10, 8),
    longitud DECIMAL(11, 8),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    CONSTRAINT fk_dispositivo_historico_dispositivos 
        FOREIGN KEY (devid) 
        REFERENCES monitoreo.dispositivos(devid) 
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    CONSTRAINT check_historico_devstatus 
        CHECK (devstatus IN (0, 1, 2, 5))
);

COMMENT ON TABLE monitoreo.dispositivo_historico IS 'Histórico de estados de dispositivos (series de tiempo)';

CREATE INDEX idx_dispositivo_historico_devid ON monitoreo.dispositivo_historico(devid);
CREATE INDEX idx_dispositivo_historico_timestamp ON monitoreo.dispositivo_historico(timestamp DESC);
CREATE INDEX idx_dispositivo_historico_devid_timestamp ON monitoreo.dispositivo_historico(devid, timestamp DESC);
CREATE INDEX idx_dispositivo_historico_devstatus ON monitoreo.dispositivo_historico(devstatus);

DO $$
BEGIN
    RAISE NOTICE '  ✓ Tabla dispositivo_historico creada con 4 índices';
    RAISE NOTICE '';
END $$;

-- ============================================================================
-- PASO 6: Crear funciones y triggers
-- ============================================================================
DO $$
BEGIN
    RAISE NOTICE 'PASO 6/7: Creando funciones y triggers...';
END $$;

-- Función para actualizar timestamp
CREATE OR REPLACE FUNCTION monitoreo.update_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Triggers para updated_at
CREATE TRIGGER trigger_dispositivos_updated_at
    BEFORE UPDATE ON monitoreo.dispositivos
    FOR EACH ROW
    EXECUTE FUNCTION monitoreo.update_timestamp();

CREATE TRIGGER trigger_interfaces_updated_at
    BEFORE UPDATE ON monitoreo.interfaces
    FOR EACH ROW
    EXECUTE FUNCTION monitoreo.update_timestamp();

-- Función para calcular ifstatus
CREATE OR REPLACE FUNCTION monitoreo.calculate_ifstatus()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.ifadmin = 1 AND NEW.ifoper = 1 THEN
        NEW.ifstatus = 1;
    ELSIF NEW.ifadmin = 1 AND NEW.ifoper > 1 THEN
        NEW.ifstatus = 2;
    ELSIF NEW.ifadmin > 1 THEN
        NEW.ifstatus = 3;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger para calcular ifstatus
CREATE TRIGGER trigger_calculate_ifstatus
    BEFORE INSERT OR UPDATE OF ifadmin, ifoper ON monitoreo.interfaces
    FOR EACH ROW
    WHEN (NEW.ifadmin IS NOT NULL AND NEW.ifoper IS NOT NULL)
    EXECUTE FUNCTION monitoreo.calculate_ifstatus();

DO $$
BEGIN
    RAISE NOTICE '  ✓ 3 funciones y 3 triggers creados';
    RAISE NOTICE '';
END $$;

-- ============================================================================
-- PASO 7: Resumen final
-- ============================================================================
DO $$
BEGIN
    RAISE NOTICE 'PASO 7/7: Verificando creación...';
    RAISE NOTICE '';
END $$;

SELECT 
    'TABLAS CREADAS' as categoria,
    COUNT(*) as cantidad
FROM information_schema.tables
WHERE table_schema = 'monitoreo'
UNION ALL
SELECT 
    'FUNCIONES CREADAS',
    COUNT(*)
FROM information_schema.routines
WHERE routine_schema = 'monitoreo'
UNION ALL
SELECT 
    'TRIGGERS CREADOS',
    COUNT(*)
FROM information_schema.triggers
WHERE trigger_schema = 'monitoreo';

DO $$
BEGIN
    RAISE NOTICE '';
    RAISE NOTICE '============================================================================';
    RAISE NOTICE '✓ ESQUEMA DE MONITOREO CREADO EXITOSAMENTE';
    RAISE NOTICE '============================================================================';
    RAISE NOTICE '';
    RAISE NOTICE 'Tablas creadas:';
    RAISE NOTICE '  1. monitoreo.dispositivos';
    RAISE NOTICE '  2. monitoreo.interfaces';
    RAISE NOTICE '  3. monitoreo.interface_historico';
    RAISE NOTICE '  4. monitoreo.dispositivo_historico';
    RAISE NOTICE '';
    RAISE NOTICE 'Próximos pasos:';
    RAISE NOTICE '  - Ejecutar 07_insert_sample_data.sql para insertar datos de prueba (OPCIONAL)';
    RAISE NOTICE '  - Configurar la conexión en el backend de VNM';
    RAISE NOTICE '  - Iniciar la sincronización con el sistema externo';
    RAISE NOTICE '';
    RAISE NOTICE '============================================================================';
END $$;
