-- ============================================================================
-- VNM - Visual Network Monitoring
-- Datos de Ejemplo para Testing
-- NOTA: Este script es OPCIONAL y solo para desarrollo/testing
-- ============================================================================

-- ============================================================================
-- DATOS DE EJEMPLO: Dispositivos
-- ============================================================================

INSERT INTO monitoreo.dispositivos (
    devid, devname, devip, operador, zona, hub, area, devstatus, 
    devstatus_lv, devstatus_lc, enterprise, modelo, latitud, longitud
) VALUES
-- Dispositivos Claro Chile - Zona Norte
(1, 'CLO-ANF-RT-01', '10.1.1.1', 'Claro Chile', 'Norte', 'Antofagasta', 'Core', 1, 
 NOW() - INTERVAL '5 minutes', NOW() - INTERVAL '2 days', 'Cisco', 'ASR 9000', -23.6509, -70.3975),

(2, 'CLO-IQQ-RT-01', '10.1.2.1', 'Claro Chile', 'Norte', 'Iquique', 'Core', 1, 
 NOW() - INTERVAL '3 minutes', NOW() - INTERVAL '1 day', 'Cisco', 'ASR 9000', -20.2140, -70.1522),

(3, 'CLO-ANF-SW-01', '10.1.1.2', 'Claro Chile', 'Norte', 'Antofagasta', 'Acceso', 1, 
 NOW() - INTERVAL '2 minutes', NOW() - INTERVAL '5 hours', 'Huawei', 'S5720', -23.6509, -70.3975),

-- Dispositivos Claro Chile - Zona Centro
(4, 'CLO-STG-RT-01', '10.2.1.1', 'Claro Chile', 'Centro', 'Santiago', 'Core', 1, 
 NOW() - INTERVAL '1 minute', NOW() - INTERVAL '12 hours', 'Cisco', 'ASR 9000', -33.4489, -70.6693),

(5, 'CLO-STG-SW-01', '10.2.1.2', 'Claro Chile', 'Centro', 'Santiago', 'Distribución', 2, 
 NOW() - INTERVAL '30 minutes', NOW() - INTERVAL '30 minutes', 'Cisco', 'Catalyst 9500', -33.4489, -70.6693),

(6, 'CLO-VLP-RT-01', '10.2.2.1', 'Claro Chile', 'Centro', 'Valparaíso', 'Core', 1, 
 NOW() - INTERVAL '4 minutes', NOW() - INTERVAL '3 days', 'Huawei', 'NE40E', -33.0472, -71.6127),

-- Dispositivos Claro Chile - Zona Sur
(7, 'CLO-CCP-RT-01', '10.3.1.1', 'Claro Chile', 'Sur', 'Concepción', 'Core', 1, 
 NOW() - INTERVAL '6 minutes', NOW() - INTERVAL '1 day', 'Cisco', 'ASR 9000', -36.8201, -73.0444),

(8, 'CLO-PUQ-RT-01', '10.3.2.1', 'Claro Chile', 'Sur', 'Punta Arenas', 'Core', 0, 
 NOW() - INTERVAL '2 hours', NOW() - INTERVAL '2 hours', 'Cisco', 'ASR 1000', -53.1638, -70.9171),

-- Dispositivo fuera de monitoreo
(9, 'CLO-TEST-SW-01', '10.9.9.1', 'Claro Chile', 'Centro', 'Santiago', 'Testing', 5, 
 NOW() - INTERVAL '1 day', NOW() - INTERVAL '1 day', 'Cisco', 'Catalyst 3850', NULL, NULL),

-- Dispositivo sin geolocalización
(10, 'CLO-ANF-SW-02', '10.1.1.3', 'Claro Chile', 'Norte', 'Antofagasta', 'Acceso', 1, 
 NOW() - INTERVAL '8 minutes', NOW() - INTERVAL '6 hours', 'Huawei', 'S5720', NULL, NULL)

ON CONFLICT (devid) DO NOTHING;

-- ============================================================================
-- DATOS DE EJEMPLO: Interfaces
-- ============================================================================

INSERT INTO monitoreo.interfaces (
    devid, devif, ifname, ifalias, ifadmin, ifoper, ifstatus, 
    iflv, iflc, ifgraficar, time, input, output, ifspeed, 
    ifindis, ifoutdis, ifinerr, ifouterr, ifutil
) VALUES
-- Interfaces del dispositivo 1 (CLO-ANF-RT-01)
(1, 101, 'GigabitEthernet0/0/0', 'Uplink a Core Santiago', 1, 1, 1, 
 NOW() - INTERVAL '1 minute', NOW() - INTERVAL '1 day', 1, NOW() - INTERVAL '1 minute', 
 850000000, 920000000, 1000, 0, 0, 0, 0, 92.00),

(1, 102, 'GigabitEthernet0/0/1', 'Enlace a IQQ-RT-01', 1, 1, 1, 
 NOW() - INTERVAL '1 minute', NOW() - INTERVAL '2 days', 1, NOW() - INTERVAL '1 minute', 
 450000000, 380000000, 1000, 0, 0, 0, 0, 45.00),

(1, 103, 'GigabitEthernet0/0/2', 'Acceso Local', 1, 1, 1, 
 NOW() - INTERVAL '1 minute', NOW() - INTERVAL '5 hours', 1, NOW() - INTERVAL '1 minute', 
 120000000, 95000000, 1000, 0, 0, 0, 0, 12.00),

(1, 104, 'GigabitEthernet0/0/3', 'Backup Link', 1, 2, 2, 
 NOW() - INTERVAL '10 minutes', NOW() - INTERVAL '10 minutes', 0, NOW() - INTERVAL '10 minutes', 
 0, 0, 1000, 0, 0, 0, 0, 0.00),

-- Interfaces del dispositivo 4 (CLO-STG-RT-01)
(4, 401, 'TenGigabitEthernet0/1/0', 'Core Principal', 1, 1, 1, 
 NOW() - INTERVAL '1 minute', NOW() - INTERVAL '6 hours', 1, NOW() - INTERVAL '1 minute', 
 8500000000, 7200000000, 10000, 0, 0, 0, 0, 85.00),

(4, 402, 'TenGigabitEthernet0/1/1', 'Enlace a Valparaíso', 1, 1, 1, 
 NOW() - INTERVAL '1 minute', NOW() - INTERVAL '3 days', 1, NOW() - INTERVAL '1 minute', 
 3200000000, 2800000000, 10000, 0, 0, 0, 0, 32.00),

(4, 403, 'TenGigabitEthernet0/1/2', 'Enlace a Concepción', 1, 1, 1, 
 NOW() - INTERVAL '1 minute', NOW() - INTERVAL '1 day', 1, NOW() - INTERVAL '1 minute', 
 5600000000, 4900000000, 10000, 5, 3, 0, 0, 56.00),

-- Interfaces del dispositivo 5 (CLO-STG-SW-01 - Caído)
(5, 501, 'GigabitEthernet1/0/1', 'Uplink Redundante', 1, 2, 2, 
 NOW() - INTERVAL '30 minutes', NOW() - INTERVAL '30 minutes', 1, NOW() - INTERVAL '30 minutes', 
 0, 0, 1000, 0, 0, 0, 0, 0.00),

(5, 502, 'GigabitEthernet1/0/2', 'Enlace Principal', 1, 2, 2, 
 NOW() - INTERVAL '30 minutes', NOW() - INTERVAL '30 minutes', 1, NOW() - INTERVAL '30 minutes', 
 0, 0, 1000, 0, 0, 0, 0, 0.00),

-- Interface con alta utilización
(7, 701, 'TenGigabitEthernet0/0/0', 'Uplink Saturado', 1, 1, 1, 
 NOW() - INTERVAL '1 minute', NOW() - INTERVAL '2 hours', 1, NOW() - INTERVAL '1 minute', 
 9500000000, 9200000000, 10000, 150, 120, 5, 3, 95.00),

-- Interface apagada administrativamente
(7, 702, 'GigabitEthernet0/0/1', 'Puerto Deshabilitado', 2, 2, 3, 
 NOW() - INTERVAL '1 day', NOW() - INTERVAL '1 day', 0, NOW() - INTERVAL '1 day', 
 0, 0, 1000, 0, 0, 0, 0, 0.00)

ON CONFLICT (devid, devif) DO NOTHING;

-- ============================================================================
-- Verificación de datos insertados
-- ============================================================================

SELECT '=== RESUMEN DE DISPOSITIVOS ===' AS seccion;

SELECT 
    devstatus,
    CASE devstatus
        WHEN 0 THEN 'No responde'
        WHEN 1 THEN 'UP'
        WHEN 2 THEN 'Caído'
        WHEN 5 THEN 'Fuera de monitoreo'
    END AS estado_descripcion,
    COUNT(*) as cantidad
FROM monitoreo.dispositivos
GROUP BY devstatus
ORDER BY devstatus;

SELECT '=== RESUMEN DE INTERFACES ===' AS seccion;

SELECT 
    ifstatus,
    CASE ifstatus
        WHEN 1 THEN 'UP'
        WHEN 2 THEN 'Down'
        WHEN 3 THEN 'Shutdown'
    END AS estado_descripcion,
    COUNT(*) as cantidad
FROM monitoreo.interfaces
GROUP BY ifstatus
ORDER BY ifstatus;

SELECT '=== TOP 5 INTERFACES MÁS UTILIZADAS ===' AS seccion;

SELECT 
    d.devname,
    i.ifname,
    i.ifalias,
    i.ifutil || '%' as utilizacion,
    i.ifspeed || ' Mbps' as velocidad
FROM monitoreo.interfaces i
JOIN monitoreo.dispositivos d ON i.devid = d.devid
WHERE i.ifgraficar = 1 AND i.ifutil IS NOT NULL
ORDER BY i.ifutil DESC
LIMIT 5;
