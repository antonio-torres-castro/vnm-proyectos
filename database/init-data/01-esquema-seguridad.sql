-- Crear esquema y tablas de seguridad
CREATE SCHEMA IF NOT EXISTS seguridad;

-- Tabla: Estados
CREATE TABLE seguridad.estados (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion VARCHAR(250)
);

-- Tabla: Permisos
CREATE TABLE seguridad.permisos (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion VARCHAR(250)
);

-- Tabla: Rol
CREATE TABLE seguridad.rol (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion VARCHAR(250)
);

-- Tabla: Rol_Permisos
CREATE TABLE seguridad.rol_permisos (
    permiso_id INT NOT NULL,
    rol_id INT NOT NULL,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    estado_id INT,
    PRIMARY KEY (permiso_id, rol_id)
);

-- Tabla: Menu_Grupo
CREATE TABLE seguridad.menu_grupo (
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
CREATE TABLE seguridad.menu (
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
CREATE TABLE seguridad.rol_menu (
    menu_id INT NOT NULL,
    rol_id INT NOT NULL,
    estado_tipo_id INT,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (menu_id, rol_id)
);

-- Tabla: Usuario
CREATE TABLE seguridad.usuario (
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
CREATE TABLE seguridad.usuario_historia (
    id SERIAL PRIMARY KEY,
    rol_id INT,
    email VARCHAR(150),
    nombre_usuario VARCHAR(100),
    clave_hash VARCHAR(255),
    estado_id INT,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    usuario_id INT
);

-- Índices
CREATE INDEX idx_usuario_email ON seguridad.usuario (email);

CREATE INDEX idx_menu_grupo_estado ON seguridad.menu_grupo (estado_id);

CREATE INDEX idx_menu_estado ON seguridad.menu (estado_id);

CREATE INDEX idx_rol_permisos_estado ON seguridad.rol_permisos (estado_id);

CREATE INDEX idx_usuario_estado ON seguridad.usuario (estado_id);