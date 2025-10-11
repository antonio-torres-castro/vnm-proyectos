-- ==========================================
-- SCRIPT DE CREACIÓN DE TABLAS - PostgreSQL 16.4
-- ==========================================
-- Configuración inicial (opcional)
CREATE SCHEMA IF NOT EXISTS seguridad AUTHORIZATION CURRENT_USER;

SET search_path TO seguridad;

-- ==========================================
-- TABLA: Estados
-- ==========================================
CREATE TABLE estados (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion VARCHAR(250)
);

-- ==========================================
-- TABLA: Permisos
-- ==========================================
CREATE TABLE permisos (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion VARCHAR(250)
);

-- ==========================================
-- TABLA: Rol
-- ==========================================
CREATE TABLE rol (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion VARCHAR(250)
);

-- ==========================================
-- TABLA: Rol_Permisos
-- ==========================================
CREATE TABLE rol_permisos (
    permiso_id INT NOT NULL REFERENCES permisos (id) ON DELETE CASCADE,
    rol_id INT NOT NULL REFERENCES rol (id) ON DELETE CASCADE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    estado_id INT REFERENCES estados (id),
    PRIMARY KEY (permiso_id, rol_id)
);

-- ==========================================
-- TABLA: Menu_Grupo
-- ==========================================
CREATE TABLE menu_grupo (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    descripcion VARCHAR(300),
    icono VARCHAR(50),
    orden INT DEFAULT 0,
    nombre_despliegue VARCHAR(150),
    estado_id INT REFERENCES estados (id),
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ==========================================
-- TABLA: Menu
-- ==========================================
CREATE TABLE menu (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    descripcion VARCHAR(300),
    url VARCHAR(100),
    icono VARCHAR(50),
    orden INT DEFAULT 0,
    nombre_despliegue VARCHAR(150),
    menu_grupo_id INT REFERENCES menu_grupo (id) ON DELETE SET NULL,
    estado_id INT REFERENCES estados (id),
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ==========================================
-- TABLA: Rol_Menu
-- ==========================================
CREATE TABLE rol_menu (
    menu_id INT NOT NULL REFERENCES menu (id) ON DELETE CASCADE,
    rol_id INT NOT NULL REFERENCES rol (id) ON DELETE CASCADE,
    estado_tipo_id INT REFERENCES estados (id),
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (menu_id, rol_id)
);

-- ==========================================
-- TABLA: Usuario
-- ==========================================
CREATE TABLE usuario (
    id SERIAL PRIMARY KEY,
    rol_id INT REFERENCES rol (id),
    email VARCHAR(150) UNIQUE NOT NULL,
    nombre_usuario VARCHAR(100) NOT NULL,
    clave_hash VARCHAR(255) NOT NULL,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_inicio TIMESTAMP,
    fecha_termino TIMESTAMP,
    fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    estado_id INT REFERENCES estados (id)
);

-- ==========================================
-- TABLA: Usuario_Historia
-- ==========================================
CREATE TABLE usuario_historia (
    id SERIAL PRIMARY KEY,
    rol_id INT REFERENCES rol (id),
    email VARCHAR(150),
    nombre_usuario VARCHAR(100),
    clave_hash VARCHAR(255),
    estado_id INT REFERENCES estados (id),
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    usuario_id INT REFERENCES usuario (id) ON DELETE CASCADE
);

-- ==========================================
-- Índices útiles
-- ==========================================
CREATE INDEX idx_usuario_email ON usuario (email);

CREATE INDEX idx_menu_grupo_estado ON menu_grupo (estado_id);

CREATE INDEX idx_menu_estado ON menu (estado_id);

CREATE INDEX idx_rol_permisos_estado ON rol_permisos (estado_id);

CREATE INDEX idx_usuario_estado ON usuario (estado_id);

-- ==========================================
-- Comentarios opcionales para documentación
-- ==========================================
COMMENT ON SCHEMA seguridad IS 'Esquema de gestión de seguridad del sistema (roles, permisos, usuarios, menús)';

COMMENT ON
TABLE estados IS 'Tabla de estados genéricos utilizados en el sistema';

COMMENT ON TABLE rol IS 'Roles de usuario dentro del sistema';

COMMENT ON
TABLE permisos IS 'Permisos individuales que se pueden asignar a roles';

COMMENT ON
TABLE rol_permisos IS 'Relación muchos a muchos entre roles y permisos';

COMMENT ON
TABLE menu IS 'Menús del sistema asociados a roles y grupos';

COMMENT ON
TABLE usuario IS 'Usuarios del sistema con su información de acceso';

COMMENT ON
TABLE usuario_historia IS 'Historial de cambios en usuarios (auditoría)';