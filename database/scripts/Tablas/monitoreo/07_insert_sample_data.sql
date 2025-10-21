-- ============================================================================
-- VNM - Visual Network Monitoring
-- Datos REALES para Inicialización de Base de Datos
-- Fuente: Datos exportados desde la red de producción
-- Generado: 2025-10-22
-- ============================================================================

-- ============================================================================
-- DATOS REALES: Dispositivos (Hub LCIS - Metropolitana)
-- Total dispositivos en archivo original: 9985
-- Dispositivos insertados: 50 (muestra representativa)
-- ============================================================================

INSERT INTO monitoreo.dispositivos (
    devid, devname, devip, operador, zona, hub, area,
    devstatus, devstatus_lv, devstatus_lc,
    enterprise, modelo, latitud, longitud
) VALUES
    -- Core y PE Routers
    (31, 'UNIVERSE_LACI01', '192.168.205.48', 'exVTR', 'Metropolitana', 'LCIS', 'MOVIL',
        1, '2025-10-09T17:49:14-03:00', '2025-04-03T00:43:08-03:00',
        'HUAWEI', 'ne40E-X3', -33.4489, -70.6693),
    
    (37, 'ASR-LCIS-PE2-CORE.vtr.cl', '192.168.139.18', 'exVTR', 'Metropolitana', 'LCIS', 'NTWKBB',
        1, '2025-10-09T17:48:00-03:00', '2025-04-03T00:43:32-03:00',
        'CISCO', 'ASR9006', -33.4489, -70.6693),
    
    (48, 'LACI_BHPE1_ASR9006.vtr.cl', '192.168.139.1', 'exVTR', 'Metropolitana', 'LCIS', 'NETWORKING',
        1, '2025-10-09T17:49:53-03:00', '2025-04-03T00:43:42-03:00',
        'CISCO', 'ASR9006', -33.4489, -70.6693),
    
    (80, 'ASR-LCIS-PE1-CORE.vtr.cl', '192.168.139.17', 'exVTR', 'Metropolitana', 'LCIS', 'NTWKBB',
        1, '2025-10-09T17:49:53-03:00', '2025-04-03T00:43:42-03:00',
        'CISCO', 'ASR9006', -33.4489, -70.6693),
    
    (1672, 'LCIS_PE1_ASR9010.vtr.cl', '200.83.0.173', 'exVTR', 'Metropolitana', 'LCIS', 'NTWKBB',
        1, '2025-10-09T17:49:53-03:00', '2025-07-24T05:06:31-04:00',
        'CISCO', 'ASR9010', -33.4489, -70.6693),
    
    (1673, 'LCIS_PE2_ASR9010.vtr.cl', '200.83.0.174', 'exVTR', 'Metropolitana', 'LCIS', 'NTWKBB',
        1, '2025-10-09T17:48:00-03:00', '2025-09-10T03:17:07-03:00',
        'CISCO', 'ASR9010', -33.4489, -70.6693),
    
    (1704, 'LCIS_RR_ASR9001', '200.83.0.129', 'exVTR', 'Metropolitana', 'LCIS', 'NTWKBB',
        1, '2025-10-09T17:49:53-03:00', '2025-04-03T00:43:42-03:00',
        'CISCO', 'ciscoASR9001', -33.4489, -70.6693),
    
    (1718, 'LCIS_P1_ASR9922.vtr.cl', '200.83.0.160', 'exVTR', 'Metropolitana', 'LCIS', 'NTWKBB',
        1, '2025-10-09T17:48:36-03:00', '2025-04-03T00:43:37-03:00',
        'CISCO', 'ciscoASR9922', -33.4489, -70.6693),
    
    -- Firewalls y Load Balancers
    (1107, 'SRX-LACI-FW-CORE_Cluster-5800', '192.168.205.46', 'exVTR', 'Metropolitana', 'LCIS', 'FWLB',
        1, '2025-10-09T17:49:14-03:00', '2025-04-03T00:43:08-03:00',
        'JUNIPER', 'SRX5800', -33.4489, -70.6693),
    
    (1741, 'FW-DAWN-SRX-1400', '192.168.38.7', 'exVTR', 'Metropolitana', 'LCIS', 'FWLB',
        1, '2025-10-09T17:48:00-03:00', '2025-04-03T00:43:34-03:00',
        'JUNIPER', 'SRX1400', -33.4489, -70.6693),
    
    (1742, 'bigip1.pro.dawn.cl', '192.168.56.5', 'exVTR', 'Metropolitana', 'LCIS', 'FWLB',
        1, '2025-10-09T17:48:36-03:00', '2025-10-09T06:03:06-03:00',
        'F5', 'bigip4200', -33.4489, -70.6693),
    
    (1743, 'bigip2.pro.dawn.cl', '192.168.56.6', 'exVTR', 'Metropolitana', 'LCIS', 'FWLB',
        1, '2025-10-09T17:49:14-03:00', '2025-10-09T08:38:06-03:00',
        'F5', 'bigip4200', -33.4489, -70.6693),
    
    (2138, 'SRX-LACI-FW.TV.CRONOS-CLUSTER-4100', '172.17.12.90', 'exVTR', 'Metropolitana', 'LCIS', 'FWLB',
        1, '2025-10-09T17:48:36-03:00', '2025-08-27T08:09:09-04:00',
        'JUNIPER', 'SRX4100', -33.4489, -70.6693),
    
    (2705, 'LACI_F5_TVCORE_1.vtr.cl', '10.68.150.3', 'exVTR', 'Metropolitana', 'LCIS', 'FWLB',
        1, '2025-10-09T17:48:01-03:00', '2025-04-03T00:43:34-03:00',
        'F5', 'bigipi2800', -33.4489, -70.6693),
    
    (2706, 'LACI_F5_TVCORE_2.vtr.cl', '10.68.150.4', 'exVTR', 'Metropolitana', 'LCIS', 'FWLB',
        1, '2025-10-09T17:48:36-03:00', '2025-04-03T00:43:37-03:00',
        'F5', 'bigipi2800', -33.4489, -70.6693),
    
    -- Switches de Acceso (CMTS)
    (1773, 'LACI_2-1i', '192.168.252.152', 'exVTR', 'Metropolitana', 'LCIS', 'ACCESO',
        1, '2025-10-09T17:48:00-03:00', '2025-04-03T00:43:33-03:00',
        'ARRIS', 'arrisE6Cer', -33.4489, -70.6693),
    
    (1774, 'LACI_2-2i', '192.168.252.153', 'exVTR', 'Metropolitana', 'LCIS', 'ACCESO',
        1, '2025-10-09T17:48:36-03:00', '2025-04-03T00:43:37-03:00',
        'ARRIS', 'arrisE6Cer', -33.4489, -70.6693),
    
    (1952, 'LACI_2-3i', '192.168.244.84', 'exVTR', 'Metropolitana', 'LCIS', 'ACCESO',
        1, '2025-10-09T17:49:54-03:00', '2025-04-03T00:43:42-03:00',
        'ARRIS', 'arrisE6Cer', -33.4489, -70.6693),
    
    (1956, 'LACI_2-4i', '192.168.244.85', 'exVTR', 'Metropolitana', 'LCIS', 'ACCESO',
        1, '2025-10-09T17:49:54-03:00', '2025-04-10T06:13:38-04:00',
        'ARRIS', 'arrisE6Cer', -33.4489, -70.6693),
    
    (1957, 'LACI_2-5i', '192.168.244.86', 'exVTR', 'Metropolitana', 'LCIS', 'ACCESO',
        1, '2025-10-09T17:48:00-03:00', '2025-04-03T00:43:33-03:00',
        'ARRIS', 'arrisE6Cer', -33.4489, -70.6693),
    
    -- Switches Nexus - Fabric
    (2585, 'LACI_SP_FABRIC_2.vtr.com', '10.68.173.74', 'exVTR', 'Metropolitana', 'LCIS', 'NTWKBB',
        1, '2025-10-09T17:48:00-03:00', '2025-04-03T00:43:33-03:00',
        'CISCO', 'cevChassisN9KC9332PQ', -33.4489, -70.6693),
    
    (2590, 'LACI_LF_CDNCON_1.vtr.com', '10.68.204.232', 'exVTR', 'Metropolitana', 'LCIS', 'NTWKBB',
        1, '2025-10-09T17:48:36-03:00', '2025-04-03T00:43:37-03:00',
        'CISCO', 'ChassisN9KC93180YCEX', -33.4489, -70.6693),
    
    (2591, 'LACI_LF_CDNCON_2.vtr.com', '10.68.204.234', 'exVTR', 'Metropolitana', 'LCIS', 'NTWKBB',
        1, '2025-10-09T17:49:14-03:00', '2025-04-03T00:43:08-03:00',
        'CISCO', 'ChassisN9KC93180YCEX', -33.4489, -70.6693),
    
    (2596, 'LACI_BL_FABRIC_1', '10.68.173.77', 'exVTR', 'Metropolitana', 'LCIS', 'NTWKBB',
        1, '2025-10-09T17:49:53-03:00', '2025-04-03T00:43:42-03:00',
        'CISCO', 'ChassisN9KC93180YCEX', -33.4489, -70.6693),
    
    (2597, 'LACI_BL_FABRIC_2.vtr.com', '10.68.173.78', 'exVTR', 'Metropolitana', 'LCIS', 'NTWKBB',
        1, '2025-10-09T17:48:01-03:00', '2025-04-03T00:43:33-03:00',
        'CISCO', 'ChassisN9KC93180YCEX', -33.4489, -70.6693),
    
    (2598, 'LACI_SP_FABRIC_1.vtr.com', '10.68.173.73', 'exVTR', 'Metropolitana', 'LCIS', 'NTWKBB',
        1, '2025-10-09T17:48:36-03:00', '2025-04-03T00:43:37-03:00',
        'CISCO', 'cevChassisN9KC9332PQ', -33.4489, -70.6693),
    
    (2600, 'LACI_LF_HZGO_1.vtr.com', '10.68.173.75', 'exVTR', 'Metropolitana', 'LCIS', 'NTWKBB',
        1, '2025-10-09T17:49:53-03:00', '2025-04-03T00:43:42-03:00',
        'CISCO', 'ChassisN9KC93180YCEX', -33.4489, -70.6693),
    
    (2601, 'LACI_LF_HZGO_2.vtr.com', '10.68.173.76', 'exVTR', 'Metropolitana', 'LCIS', 'NTWKBB',
        1, '2025-10-09T17:48:01-03:00', '2025-04-03T00:43:33-03:00',
        'CISCO', 'ChassisN9KC93180YCEX', -33.4489, -70.6693),
    
    -- Switches de Televisión
    (1914, 'LACI_SW_NPVR_1', '10.68.172.196', 'exVTR', 'Metropolitana', 'LCIS', 'NTWKBB',
        1, '2025-10-09T17:48:36-03:00', '2025-04-03T00:43:37-03:00',
        'CISCO', 'cevChassisN3KC31128PQ', -33.4489, -70.6693),
    
    (1915, 'LACI_SW_NPVR_2', '10.68.172.197', 'exVTR', 'Metropolitana', 'LCIS', 'NTWKBB',
        1, '2025-10-09T17:49:14-03:00', '2025-04-03T00:43:08-03:00',
        'CISCO', 'cevChassisN3KC31128PQ', -33.4489, -70.6693),
    
    (2602, 'LACI_SW_ATEME_1', '192.168.196.212', 'exVTR', 'Metropolitana', 'LCIS', 'NTWKBB',
        1, '2025-10-09T17:48:36-03:00', '2025-04-03T00:43:37-03:00',
        'CISCO', 'cevChassisN3KC31128PQ', -33.4489, -70.6693),
    
    (2603, 'LACI_SW_ATEME_2', '192.168.196.213', 'exVTR', 'Metropolitana', 'LCIS', 'NTWKBB',
        1, '2025-10-09T17:49:14-03:00', '2025-04-03T00:43:08-03:00',
        'CISCO', 'cevChassisN3KC31128PQ', -33.4489, -70.6693),
    
    -- Switches QFX - Juniper
    (4251, 'LCIS_SW1_QFX_PE1', '192.168.252.2', 'exVTR', 'Metropolitana', 'LCIS', 'NTWKBB',
        1, '2025-10-09T17:49:14-03:00', '2025-04-03T00:43:08-03:00',
        'JUNIPER', 'QFX5120-32C', -33.4489, -70.6693),
    
    (4252, 'LCIS_SW2_QFX5120_PE1', '192.168.252.6', 'exVTR', 'Metropolitana', 'LCIS', 'NTWKBB',
        1, '2025-10-09T17:49:53-03:00', '2025-04-03T00:43:42-03:00',
        'JUNIPER', 'QFX5120-48Y', -33.4489, -70.6693),
    
    (4253, 'LCIS_SW3_QFX5120_PE1', '192.168.252.18', 'exVTR', 'Metropolitana', 'LCIS', 'NTWKBB',
        1, '2025-10-09T17:48:01-03:00', '2025-04-03T00:43:33-03:00',
        'JUNIPER', 'QFX5120-48Y', -33.4489, -70.6693),
    
    (4256, 'LCIS_SW1_QFX5120_PE2', '192.168.252.106', 'exVTR', 'Metropolitana', 'LCIS', 'NTWKBB',
        1, '2025-10-09T17:49:53-03:00', '2025-04-03T00:43:42-03:00',
        'JUNIPER', 'QFX5120-32C', -33.4489, -70.6693),
    
    (4257, 'LCIS_SW2_QFX5120_PE2', '192.168.252.110', 'exVTR', 'Metropolitana', 'LCIS', 'NTWKBB',
        1, '2025-10-09T17:48:01-03:00', '2025-04-03T00:43:33-03:00',
        'JUNIPER', 'QFX5120-48Y', -33.4489, -70.6693),
    
    -- Switches MX960 - Juniper
    (4249, 'LCIS_PE1_MX960-re0', '200.83.0.66', 'exVTR', 'Metropolitana', 'LCIS', 'NTWKBB',
        1, '2025-10-09T17:48:01-03:00', '2025-04-03T00:43:33-03:00',
        'JUNIPER', 'MX960', -33.4489, -70.6693),
    
    (4250, 'LCIS_PE2_MX960-re0', '200.83.0.67', 'exVTR', 'Metropolitana', 'LCIS', 'NTWKBB',
        1, '2025-10-09T17:48:36-03:00', '2025-04-03T00:43:38-03:00',
        'JUNIPER', 'MX960', -33.4489, -70.6693),
    
    (4126, 'LCIS_BORDE1_MX960', '200.83.0.100', 'exVTR', 'Metropolitana', 'LCIS', 'ISP',
        1, '2025-10-09T17:48:36-03:00', '2025-04-03T00:43:37-03:00',
        'JUNIPER', 'MX960', -33.4489, -70.6693),
    
    -- Dispositivos Hub INDE
    (29, 'UNIVERSE_INDE01', '192.168.205.166', 'exVTR', 'Metropolitana', 'INDE', 'MOVIL',
        1, '2025-10-09T17:48:01-03:00', '2025-04-03T00:43:33-03:00',
        'HUAWEI', 'ne40E-X3', -33.4489, -70.6693),
    
    (35, 'SRX-INDE-FW-CORE_Cluster-5800', '192.168.205.164', 'exVTR', 'Metropolitana', 'INDE', 'FWLB',
        1, '2025-10-09T17:49:14-03:00', '2025-04-03T00:43:08-03:00',
        'JUNIPER', 'SRX5800', -33.4489, -70.6693),
    
    (38, 'ASR-INDE-PE1-CORE.vtr.cl', '192.168.139.19', 'exVTR', 'Metropolitana', 'INDE', 'NTWKBB',
        1, '2025-10-09T17:48:36-03:00', '2025-04-03T00:43:37-03:00',
        'CISCO', 'ASR9006', -33.4489, -70.6693),
    
    (39, 'ASR-INDE-PE2-CORE.vtr.cl', '192.168.139.20', 'exVTR', 'Metropolitana', 'INDE', 'NTWKBB',
        1, '2025-10-09T17:49:14-03:00', '2025-04-03T00:43:08-03:00',
        'CISCO', 'ASR9006', -33.4489, -70.6693),
    
    (49, 'INDE-AGG01-PE1', '192.168.139.3', 'exVTR', 'Metropolitana', 'INDE', 'NTWKBB',
        1, '2025-10-09T17:48:01-03:00', '2025-10-07T01:05:38-03:00',
        'CISCO', 'ASR9006', -33.4489, -70.6693),
    
    (50, 'INDE-AGG02-PE2', '192.168.139.4', 'exVTR', 'Metropolitana', 'INDE', 'NETWORKING',
        1, '2025-10-09T17:48:36-03:00', '2025-10-05T23:34:22-03:00',
        'CISCO', 'ASR9006', -33.4489, -70.6693),
    
    (1668, 'INDE_PE1_ASR9010.vtr.cl', '200.83.0.194', 'exVTR', 'Metropolitana', 'INDE', 'NTWKBB',
        1, '2025-10-09T17:49:53-03:00', '2025-07-28T11:52:39-04:00',
        'CISCO', 'ASR9010', -33.4489, -70.6693),
    
    (1669, 'INDE_PE2_ASR9010', '200.83.0.195', 'exVTR', 'Metropolitana', 'INDE', 'NTWKBB',
        1, '2025-10-09T17:48:01-03:00', '2025-04-07T00:57:04-04:00',
        'CISCO', 'ASR9010', -33.4489, -70.6693),
    
    (1705, 'INDE_RR_ASR9001', '200.83.0.130', 'exVTR', 'Metropolitana', 'INDE', 'NTWKBB',
        1, '2025-10-09T17:48:01-03:00', '2025-04-03T00:43:33-03:00',
        'CISCO', 'ciscoASR9001', -33.4489, -70.6693),
    
    -- Dispositivos con problemas / Fuera de servicio
    (47, 'LACI_BHPE2_ASR9006.vtr.cl', '192.168.139.2', 'exVTR', 'Metropolitana', 'LCIS', 'NETWORKING',
        0, '2023-09-05T23:42:04-03:00', '2023-09-06T01:42:54-03:00',
        'CISCO', 'ASR9006', -33.4489, -70.6693),
    
    (2990, 'SW3560-LCIS12', '192.168.171.205', 'exVTR', 'Metropolitana', 'LCIS', 'NTWKBB',
        2, '2025-08-14T16:03:53-04:00', '2025-08-14T16:07:13-04:00',
        'CISCO', 'catalyst3560G48TS', -33.4489, -70.6693),
    
    (4113, 'LACI_SW_CORE_VIDEO_DAA_01', '10.68.121.160', 'exVTR', 'Metropolitana', 'LCIS', 'INGNETWORKING',
        0, '2025-08-01T02:24:17-04:00', '2025-08-01T02:27:37-04:00',
        'CISCO', 'ChassisN9KC93180YCEX', -33.4489, -70.6693)

ON CONFLICT (devid) DO UPDATE SET
    devname = EXCLUDED.devname,
    devip = EXCLUDED.devip,
    devstatus = EXCLUDED.devstatus,
    devstatus_lv = EXCLUDED.devstatus_lv,
    devstatus_lc = EXCLUDED.devstatus_lc,
    zona = EXCLUDED.zona,
    hub = EXCLUDED.hub,
    area = EXCLUDED.area;

-- ============================================================================
-- DATOS REALES: Interfaces del UNIVERSE_LACI01 (devid=31)
-- Total interfaces: 30
-- ============================================================================

INSERT INTO monitoreo.interfaces (
    devid, devif, ifname, ifalias, ifadmin, ifoper, ifstatus,
    iflv, iflc, ifgraficar, time,
    input, output, ifspeed, ifindis, ifoutdis, ifinerr, ifouterr, ifutil
) VALUES
    -- Interfaces administrativas y loopback
    (31, 863456, 'Console0/0/0', 'HUAWEI, Console0/0/0 Interface', 1, 1, 1,
        '2025-10-09T13:13:46-03:00', '2023-09-11T13:41:06-03:00', 0, NULL,
        NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
    
    (31, 863429, 'InLoopBack0', 'HUAWEI, InLoopBack0 Interface', 1, 1, 1,
        '2025-10-09T13:13:46-03:00', '2023-09-11T13:41:06-03:00', 0, NULL,
        NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
    
    (31, 863443, 'NULL0', 'NO_USAR', 1, 1, 1,
        '2025-10-09T13:13:46-03:00', '2023-09-11T13:41:06-03:00', 0, NULL,
        NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
    
    -- Interfaces principales hacia Core
    (31, 863750, 'GigabitEthernet1/0/0', 'TO_PE01_ASR9006_TE1/0/2_GP', 1, 2, 2,
        '2025-10-09T13:13:47-03:00', '2023-09-11T13:41:08-03:00', 0, NULL,
        NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
    
    (31, 863780, 'GigabitEthernet1/1/0', 'TO_PE02_ASR9006_TE1/0/2_GP', 1, 2, 2,
        '2025-10-09T13:13:47-03:00', '2023-09-11T13:41:08-03:00', 0, NULL,
        NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
    
    -- Interfaces hacia SBC
    (31, 863520, 'GigabitEthernet2/0/1', 'TO -LACI_PE2_ASR9010-INT-GI0/7/1/2-SBC', 1, 2, 2,
        '2025-10-09T13:13:46-03:00', '2023-09-11T13:41:07-03:00', 0, NULL,
        NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
    
    -- Interfaces hacia Firewalls - EN USO Y GRAFICADAS
    (31, 863554, 'GigabitEthernet2/0/3', 'SRX-LACI-FW1-CORE_GE_0/1/8', 1, 1, 1,
        '2025-10-09T17:43:34-03:00', '2024-12-15T11:47:11-03:00', 1, '2025-10-09T17:30:00-03:00',
        0, 140, 1000, 0, 0, 0, 0, 0.01),
    
    (31, 863577, 'GigabitEthernet2/0/4', 'SRX-LACI-FW2-CORE_GE_12/1/8', 1, 1, 1,
        '2025-10-09T17:43:28-03:00', '2024-12-15T11:25:36-03:00', 1, '2025-10-09T17:30:00-03:00',
        0, 142, 1000, 0, 0, 0, 0, 0.01),
    
    -- Interface de gestión - EN USO Y GRAFICADA
    (31, 863708, 'GigabitEthernet2/0/10', 'CONEXION_O&M_TEMPORAL', 1, 1, 1,
        '2025-10-09T17:40:51-03:00', '2025-09-29T08:58:07-03:00', 1, '2025-10-09T17:35:00-03:00',
        14861, 1535, 1000, 0, 0, 0, 0, 1.46),
    
    -- VLANs de servicio - EN USO Y GRAFICADAS
    (31, 863819, 'Vlanif500', 'DATACOMM_O&M', 1, 1, 1,
        '2025-10-09T17:41:55-03:00', '2025-09-29T08:58:08-03:00', 1, '2025-10-09T17:35:00-03:00',
        0, 0, 1000, 0, 0, 0, 0, 0.00),
    
    (31, 863875, 'Vlanif346', 'DRA_to_FW', 1, 1, 1,
        '2025-10-09T17:42:31-03:00', '2024-12-03T11:50:55-03:00', 1, '2025-10-09T17:30:00-03:00',
        0, 0, 1000, 0, 0, 0, 0, 0.00),
    
    (31, 863889, 'Vlanif348', 'SIG_3G_to_FW', 1, 1, 1,
        '2025-10-09T17:43:28-03:00', '2024-12-15T11:50:56-03:00', 1, '2025-10-09T17:30:00-03:00',
        0, 0, 1000, 0, 0, 0, 0, 0.00),
    
    -- Interfaces deshabilitadas
    (31, 863469, 'GigabitEthernet0/0/0', 'NO USAR', 2, 2, 3,
        '2025-10-09T13:13:46-03:00', '2023-09-11T10:02:59-03:00', 0, NULL,
        NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
    
    (31, 863764, 'GigabitEthernet1/0/1', 'to_MOVISTAR_MMT2', 2, 2, 3,
        '2025-10-09T13:13:47-03:00', '2023-09-11T10:03:01-03:00', 0, NULL,
        NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
    
    (31, 863801, 'GigabitEthernet1/1/1', 'TO_CONCERT_QUICRTAGG1:Te7/3', 2, 2, 3,
        '2025-10-09T13:13:47-03:00', '2023-09-11T10:03:02-03:00', 0, NULL,
        NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
    
    (31, 863491, 'GigabitEthernet2/0/0', 'BICS', 2, 2, 3,
        '2025-10-09T13:13:46-03:00', '2023-09-11T10:02:59-03:00', 0, NULL,
        NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
    
    (31, 863541, 'GigabitEthernet2/0/2', 'libre', 2, 2, 3,
        '2025-10-09T13:13:46-03:00', '2023-09-11T10:02:59-03:00', 0, NULL,
        NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
    
    (31, 863601, 'GigabitEthernet2/0/5', 'libre', 2, 2, 3,
        '2025-10-09T13:13:47-03:00', '2023-09-11T10:03:00-03:00', 0, NULL,
        NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
    
    (31, 863613, 'GigabitEthernet2/0/6', 'libre', 2, 2, 3,
        '2025-10-09T13:13:47-03:00', '2023-09-11T10:03:00-03:00', 0, NULL,
        NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
    
    (31, 863630, 'GigabitEthernet2/0/7', 'libre', 2, 2, 3,
        '2025-10-09T13:13:47-03:00', '2023-09-11T10:03:00-03:00', 0, NULL,
        NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
    
    (31, 863651, 'GigabitEthernet2/0/8', 'libre', 2, 2, 3,
        '2025-10-09T13:13:47-03:00', '2023-09-11T10:03:01-03:00', 0, NULL,
        NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
    
    (31, 863677, 'GigabitEthernet2/0/9', 'libre', 2, 2, 3,
        '2025-10-09T13:13:47-03:00', '2023-09-11T10:03:01-03:00', 0, NULL,
        NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
    
    (31, 863724, 'GigabitEthernet2/0/11', 'HUAWEI, GigabitEthernet2/0/11 Interface', 2, 2, 3,
        '2025-10-09T13:13:47-03:00', '2023-09-11T10:03:01-03:00', 0, NULL,
        NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
    
    -- Sub-interfaces y VLANs fuera de servicio
    (31, 863966, 'GigabitEthernet1/0/1.1100', 'to_MOVISTAR_SIG_3G', 1, 2, 2,
        '2025-10-09T13:13:47-03:00', '2023-09-11T13:41:10-03:00', 0, NULL,
        NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
    
    (31, 863949, 'GigabitEthernet1/0/1.903', 'to_MOVISTAR_GnGp', 1, 2, 2,
        '2025-10-09T13:13:47-03:00', '2023-09-11T13:41:10-03:00', 0, NULL,
        NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
    
    (31, 863913, 'GigabitEthernet1/0/1.904', 'to_MOVISTAR_DRA', 1, 2, 2,
        '2025-10-09T13:13:47-03:00', '2023-09-11T13:41:09-03:00', 0, NULL,
        NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
    
    (31, 863834, 'Vlanif1000', 'Servicio_Roaming', 1, 2, 2,
        '2025-10-09T13:13:47-03:00', '2023-09-11T13:41:09-03:00', 0, NULL,
        NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
    
    (31, 863984, 'Vlanif315', 'SIG_3G_to_FW', 2, 2, 3,
        '2025-10-09T13:13:47-03:00', '2023-09-11T10:03:02-03:00', 0, NULL,
        NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
    
    -- Interfaces virtuales
    (31, 863853, 'Virtual-Template0', 'HUAWEI, Virtual-Template0 Interface', 1, 1, 1,
        '2025-10-09T13:13:47-03:00', '2023-09-11T13:41:09-03:00', 0, NULL,
        NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
    
    (31, 863475, 'Aux0/0/1', 'NO_USAR', 1, 2, 2,
        '2025-10-09T13:13:46-03:00', '2023-09-11T13:41:06-03:00', 0, NULL,
        NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL)

ON CONFLICT (devid, devif) DO UPDATE SET
    ifname = EXCLUDED.ifname,
    ifalias = EXCLUDED.ifalias,
    ifstatus = EXCLUDED.ifstatus,
    iflv = EXCLUDED.iflv,
    ifgraficar = EXCLUDED.ifgraficar,
    time = EXCLUDED.time,
    input = EXCLUDED.input,
    output = EXCLUDED.output,
    ifutil = EXCLUDED.ifutil;

-- ============================================================================
-- Consultas de Verificación
-- ============================================================================

DO $$ 
BEGIN 
    RAISE NOTICE '';
    RAISE NOTICE '====================================================================';
    RAISE NOTICE 'RESUMEN DE DATOS INSERTADOS';
    RAISE NOTICE '====================================================================';
    RAISE NOTICE '';
END $$;

DO $$ 
BEGIN 
    RAISE NOTICE '=== DISPOSITIVOS POR ESTADO ===';
END $$;

SELECT 
    devstatus,
    CASE devstatus
        WHEN 0 THEN 'No responde'
        WHEN 1 THEN 'UP'
        WHEN 2 THEN 'Caído'
        WHEN 5 THEN 'Fuera de monitoreo'
        ELSE 'Desconocido'
    END AS estado_descripcion,
    COUNT(*) as cantidad
FROM monitoreo.dispositivos
GROUP BY devstatus
ORDER BY devstatus;

DO $$ 
BEGIN 
    RAISE NOTICE '';
    RAISE NOTICE '=== DISPOSITIVOS POR HUB ===';
END $$;

SELECT 
    hub,
    zona,
    COUNT(*) as cantidad,
    COUNT(*) FILTER (WHERE devstatus = 1) as activos,
    COUNT(*) FILTER (WHERE devstatus IN (0,2)) as caídos
FROM monitoreo.dispositivos
GROUP BY hub, zona
ORDER BY hub, zona;

DO $$ 
BEGIN 
    RAISE NOTICE '';
    RAISE NOTICE '=== INTERFACES POR ESTADO ===';
END $$;

SELECT 
    ifstatus,
    CASE ifstatus
        WHEN 1 THEN 'UP'
        WHEN 2 THEN 'Down'
        WHEN 3 THEN 'Shutdown'
        ELSE 'Desconocido'
    END AS estado_descripcion,
    COUNT(*) as cantidad,
    COUNT(*) FILTER (WHERE ifgraficar = 1) as graficadas,
    ROUND(AVG(ifutil) FILTER (WHERE ifutil IS NOT NULL), 2) as util_promedio
FROM monitoreo.interfaces
GROUP BY ifstatus
ORDER BY ifstatus;

DO $$ 
BEGIN 
    RAISE NOTICE '';
    RAISE NOTICE '=== INTERFACES ACTIVAS Y GRAFICADAS ===';
END $$;

SELECT 
    d.devname,
    i.ifname,
    i.ifalias,
    COALESCE(i.ifutil, 0) || '%' as utilizacion,
    COALESCE(i.ifspeed, 0) || ' Mbps' as velocidad,
    COALESCE(i.input, 0) as input_bps,
    COALESCE(i.output, 0) as output_bps
FROM monitoreo.interfaces i
JOIN monitoreo.dispositivos d ON i.devid = d.devid
WHERE i.ifgraficar = 1 AND i.ifstatus = 1
ORDER BY i.ifutil DESC NULLS LAST
LIMIT 10;

DO $$ 
BEGIN 
    RAISE NOTICE '';
    RAISE NOTICE '====================================================================';
    RAISE NOTICE 'Datos insertados correctamente';
    RAISE NOTICE '====================================================================';
END $$;
