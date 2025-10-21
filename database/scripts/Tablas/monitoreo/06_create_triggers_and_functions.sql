-- ============================================================================
-- VNM - Visual Network Monitoring
-- Funciones y Triggers del Esquema de Monitoreo
-- ============================================================================

-- ============================================================================
-- FUNCIÓN: Actualizar timestamp de updated_at automáticamente
-- ============================================================================

CREATE OR REPLACE FUNCTION monitoreo.update_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

COMMENT ON FUNCTION monitoreo.update_timestamp() IS 'Función para actualizar automáticamente el campo updated_at';

-- ============================================================================
-- TRIGGER: Actualizar updated_at en dispositivos
-- ============================================================================

CREATE TRIGGER trigger_dispositivos_updated_at
    BEFORE UPDATE ON monitoreo.dispositivos
    FOR EACH ROW
    EXECUTE FUNCTION monitoreo.update_timestamp();

COMMENT ON TRIGGER trigger_dispositivos_updated_at ON monitoreo.dispositivos IS 
'Actualiza automáticamente updated_at al modificar un dispositivo';

-- ============================================================================
-- TRIGGER: Actualizar updated_at en interfaces
-- ============================================================================

CREATE TRIGGER trigger_interfaces_updated_at
    BEFORE UPDATE ON monitoreo.interfaces
    FOR EACH ROW
    EXECUTE FUNCTION monitoreo.update_timestamp();

COMMENT ON TRIGGER trigger_interfaces_updated_at ON monitoreo.interfaces IS 
'Actualiza automáticamente updated_at al modificar una interfaz';

-- ============================================================================
-- FUNCIÓN: Calcular estado de interfaz automáticamente
-- ============================================================================

CREATE OR REPLACE FUNCTION monitoreo.calculate_ifstatus()
RETURNS TRIGGER AS $$
BEGIN
    -- Calcular ifstatus basado en ifadmin e ifoper
    -- 1 = UP (ifadmin=1, ifoper=1)
    -- 2 = Down (ifadmin=1, ifoper>1)
    -- 3 = Shutdown (ifadmin>1)
    
    IF NEW.ifadmin = 1 AND NEW.ifoper = 1 THEN
        NEW.ifstatus = 1;  -- UP
    ELSIF NEW.ifadmin = 1 AND NEW.ifoper > 1 THEN
        NEW.ifstatus = 2;  -- Down
    ELSIF NEW.ifadmin > 1 THEN
        NEW.ifstatus = 3;  -- Shutdown
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

COMMENT ON FUNCTION monitoreo.calculate_ifstatus() IS 
'Calcula automáticamente ifstatus basado en ifadmin e ifoper';

-- ============================================================================
-- TRIGGER: Calcular ifstatus automáticamente
-- ============================================================================

CREATE TRIGGER trigger_calculate_ifstatus
    BEFORE INSERT OR UPDATE OF ifadmin, ifoper ON monitoreo.interfaces
    FOR EACH ROW
    WHEN (NEW.ifadmin IS NOT NULL AND NEW.ifoper IS NOT NULL)
    EXECUTE FUNCTION monitoreo.calculate_ifstatus();

COMMENT ON TRIGGER trigger_calculate_ifstatus ON monitoreo.interfaces IS 
'Calcula automáticamente ifstatus cuando cambian ifadmin o ifoper';

-- ============================================================================
-- FUNCIÓN: Registrar cambios de estado en histórico
-- ============================================================================

CREATE OR REPLACE FUNCTION monitoreo.log_dispositivo_estado_change()
RETURNS TRIGGER AS $$
BEGIN
    -- Solo registrar si el estado cambió
    IF (TG_OP = 'UPDATE' AND OLD.devstatus IS DISTINCT FROM NEW.devstatus) OR TG_OP = 'INSERT' THEN
        INSERT INTO monitoreo.dispositivo_historico (devid, timestamp, devstatus, latitud, longitud)
        VALUES (NEW.devid, NOW(), NEW.devstatus, NEW.latitud, NEW.longitud);
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

COMMENT ON FUNCTION monitoreo.log_dispositivo_estado_change() IS 
'Registra automáticamente cambios de estado de dispositivos en el histórico';

-- ============================================================================
-- TRIGGER: Registrar cambios de estado de dispositivos (OPCIONAL - COMENTADO)
-- ============================================================================

-- DESCOMENTAR SI SE DESEA TRACKING AUTOMÁTICO
/*
CREATE TRIGGER trigger_log_dispositivo_estado
    AFTER INSERT OR UPDATE OF devstatus ON monitoreo.dispositivos
    FOR EACH ROW
    EXECUTE FUNCTION monitoreo.log_dispositivo_estado_change();

COMMENT ON TRIGGER trigger_log_dispositivo_estado ON monitoreo.dispositivos IS 
'Registra automáticamente cambios de estado en dispositivo_historico';
*/

-- Verificación de funciones
SELECT 
    routine_name,
    routine_type,
    data_type
FROM information_schema.routines
WHERE routine_schema = 'monitoreo'
ORDER BY routine_name;

-- Verificación de triggers
SELECT 
    trigger_name,
    event_manipulation,
    event_object_table,
    action_timing
FROM information_schema.triggers
WHERE trigger_schema = 'monitoreo'
ORDER BY event_object_table, trigger_name;
