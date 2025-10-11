-- Este archivo se ejecutará automáticamente al iniciar el contenedor
-- PostGIS ya viene instalado en la imagen postgis/postgis

-- Crear esquemas
CREATE SCHEMA IF NOT EXISTS sistema;

CREATE SCHEMA IF NOT EXISTS monitoreo;

-- Mensaje de confirmación
SELECT 'Base de datos con PostGIS inicializada correctamente' as status;