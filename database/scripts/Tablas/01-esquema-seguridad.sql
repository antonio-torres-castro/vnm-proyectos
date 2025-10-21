-- Crear esquema y tablas de seguridad (idempotente)
CREATE SCHEMA IF NOT EXISTS seguridad;

-- Tabla: Estados
CREATE TABLE IF NOT EXISTS seguridad.estados (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion VARCHAR(250)
);

-- Tabla: Permisos
CREATE TABLE IF NOT EXISTS seguridad.permisos (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion VARCHAR(250)
);

-- Tabla: Rol
CREATE TABLE IF NOT EXISTS seguridad.rol (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion VARCHAR(250)
);

-- Tabla: Rol_Permisos
CREATE TABLE IF NOT EXISTS seguridad.rol_permisos (
    permiso_id INT NOT NULL,
    rol_id INT NOT NULL,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    estado_id INT,
    PRIMARY KEY (permiso_id, rol_id)
);

-- Tabla: Menu_Grupo
CREATE TABLE IF NOT EXISTS seguridad.menu_grupo (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    descripcion VARCHAR(300),
    icono VARCHAR(50),
    orden INT DEFAULT 0,
    nombre_despliegue VARCHAR(150),
    estado_id INT,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla: Menu
CREATE TABLE IF NOT EXISTS seguridad.menu (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    descripcion VARCHAR(300),
    url VARCHAR(100),
    icono VARCHAR(50),
    orden INT DEFAULT 0,
    nombre_despliegue VARCHAR(150),
    menu_grupo_id INT,
    estado_id INT,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla: Rol_Menu
CREATE TABLE IF NOT EXISTS seguridad.rol_menu (
    menu_id INT NOT NULL,
    rol_id INT NOT NULL,
    estado_tipo_id INT,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (menu_id, rol_id)
);

-- Tabla: Usuario
CREATE TABLE IF NOT EXISTS seguridad.usuario (
    id SERIAL PRIMARY KEY,
    rol_id INT,
    email VARCHAR(150) UNIQUE NOT NULL,
    nombre_usuario VARCHAR(100) NOT NULL,
    clave_hash VARCHAR(255) NOT NULL,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_inicio TIMESTAMP,
    fecha_termino TIMESTAMP,
    fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    estado_id INT
);

-- Tabla: Usuario_Historia
CREATE TABLE IF NOT EXISTS seguridad.usuario_historia (
    id SERIAL PRIMARY KEY,
    rol_id INT,
    email VARCHAR(150),
    nombre_usuario VARCHAR(100),
    clave_hash VARCHAR(255),
    estado_id INT,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    usuario_id INT
);

-- Índices (idempotentes)
DO $$ 
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_indexes WHERE indexname = 'idx_usuario_email') THEN
        CREATE INDEX idx_usuario_email ON seguridad.usuario (email);
    END IF;
    
    IF NOT EXISTS (SELECT 1 FROM pg_indexes WHERE indexname = 'idx_menu_grupo_estado') THEN
        CREATE INDEX idx_menu_grupo_estado ON seguridad.menu_grupo (estado_id);
    END IF;
    
    IF NOT EXISTS (SELECT 1 FROM pg_indexes WHERE indexname = 'idx_menu_estado') THEN
        CREATE INDEX idx_menu_estado ON seguridad.menu (estado_id);
    END IF;
    
    IF NOT EXISTS (SELECT 1 FROM pg_indexes WHERE indexname = 'idx_rol_permisos_estado') THEN
        CREATE INDEX idx_rol_permisos_estado ON seguridad.rol_permisos (estado_id);
    END IF;
    
    IF NOT EXISTS (SELECT 1 FROM pg_indexes WHERE indexname = 'idx_usuario_estado') THEN
        CREATE INDEX idx_usuario_estado ON seguridad.usuario (estado_id);
    END IF;
END $$;