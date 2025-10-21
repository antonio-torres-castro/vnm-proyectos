-- ============================================================================
-- VNM - Visual Network Monitoring
-- Script de Creación del Esquema de Monitoreo
-- Autor: MiniMax Agent
-- Fecha: 2025-10-22
-- Base de Datos: PostgreSQL
-- ============================================================================

-- Crear el esquema monitoreo si no existe
CREATE SCHEMA IF NOT EXISTS monitoreo;

-- Comentario del esquema
COMMENT ON SCHEMA monitoreo IS 'Esquema para datos de monitoreo de red - Solo lectura desde sistema externo';

-- Verificación
SELECT schema_name 
FROM information_schema.schemata 
WHERE schema_name = 'monitoreo';
