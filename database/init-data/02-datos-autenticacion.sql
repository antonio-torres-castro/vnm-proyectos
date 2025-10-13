-- Datos iniciales para el sistema de autenticación (idempotente)

-- Insertar estados básicos solo si no existen
INSERT INTO
    seguridad.estados (id, nombre, descripcion)
SELECT 1, 'Creado', 'Registro creado en el sistema'
WHERE
    NOT EXISTS (
        SELECT 1
        FROM seguridad.estados
        WHERE
            id = 1
    );

INSERT INTO
    seguridad.estados (id, nombre, descripcion)
SELECT 2, 'Activo', 'Registro activo en el sistema'
WHERE
    NOT EXISTS (
        SELECT 1
        FROM seguridad.estados
        WHERE
            id = 2
    );

INSERT INTO
    seguridad.estados (id, nombre, descripcion)
SELECT 3, 'Inactivo', 'Registro inactivo en el sistema'
WHERE
    NOT EXISTS (
        SELECT 1
        FROM seguridad.estados
        WHERE
            id = 3
    );

INSERT INTO
    seguridad.estados (id, nombre, descripcion)
SELECT 4, 'Eliminado', 'Registro eliminado logicamente en el sistema'
WHERE
    NOT EXISTS (
        SELECT 1
        FROM seguridad.estados
        WHERE
            id = 4
    );

INSERT INTO
    seguridad.estados (id, nombre, descripcion)
SELECT 5, 'Iniciado', 'Proceso o Vigencia en ambito del modulo respectivo a iniciado'
WHERE
    NOT EXISTS (
        SELECT 1
        FROM seguridad.estados
        WHERE
            id = 5
    );

INSERT INTO
    seguridad.estados (id, nombre, descripcion)
SELECT 6, 'Terminado', 'Proceso o Vigencia en ambito del modulo respectivo a iniciado'
WHERE
    NOT EXISTS (
        SELECT 1
        FROM seguridad.estados
        WHERE
            id = 6
    );

INSERT INTO
    seguridad.estados (id, nombre, descripcion)
SELECT 6, 'Rechazado', 'Proceso o Tarea en ambito del modulo respectivo rechazada'
WHERE
    NOT EXISTS (
        SELECT 1
        FROM seguridad.estados
        WHERE
            id = 6
    );

INSERT INTO
    seguridad.estados (id, nombre, descripcion)
SELECT 6, 'Aprobado', 'Proceso o Tarea en ambito del modulo respectivo rechazada'
WHERE
    NOT EXISTS (
        SELECT 1
        FROM seguridad.estados
        WHERE
            id = 6
    );

-- Insertar roles del sistema solo si no existen
INSERT INTO
    seguridad.rol (id, nombre, descripcion)
SELECT 1, 'Administrador', 'Acceso completo al sistema'
WHERE
    NOT EXISTS (
        SELECT 1
        FROM seguridad.rol
        WHERE
            id = 1
    );

INSERT INTO
    seguridad.rol (id, nombre, descripcion)
SELECT 2, 'Supervisor', 'Acceso de supervisión y reportes'
WHERE
    NOT EXISTS (
        SELECT 1
        FROM seguridad.rol
        WHERE
            id = 2
    );

INSERT INTO
    seguridad.rol (id, nombre, descripcion)
SELECT 3, 'Ejecutor', 'Acceso básico de ejecución'
WHERE
    NOT EXISTS (
        SELECT 1
        FROM seguridad.rol
        WHERE
            id = 3
    );

-- Insertar permisos solo si no existen Lectura, Creación, Modificación, Exportación
INSERT INTO
    seguridad.permisos (id, nombre, descripcion)
SELECT 1, 'Lectura', 'Permiso de lectura de datos'
WHERE
    NOT EXISTS (
        SELECT 1
        FROM seguridad.permisos
        WHERE
            id = 1
    );

INSERT INTO
    seguridad.permisos (id, nombre, descripcion)
SELECT 2, 'Creación', 'Permiso de creación de registros'
WHERE
    NOT EXISTS (
        SELECT 1
        FROM seguridad.permisos
        WHERE
            id = 2
    );

INSERT INTO
    seguridad.permisos (id, nombre, descripcion)
SELECT 3, 'Modificación', 'Permiso de modificación de registros'
WHERE
    NOT EXISTS (
        SELECT 1
        FROM seguridad.permisos
        WHERE
            id = 3
    );

INSERT INTO
    seguridad.permisos (id, nombre, descripcion)
SELECT 4, 'Exportación', 'Permiso de exportación de datos'
WHERE
    NOT EXISTS (
        SELECT 1
        FROM seguridad.permisos
        WHERE
            id = 4
    );

-- Asignar permisos a roles solo si no existen
INSERT INTO
    seguridad.rol_permisos (rol_id, permiso_id, estado_id)
SELECT 1, 1, 1
WHERE
    NOT EXISTS (
        SELECT 1
        FROM seguridad.rol_permisos
        WHERE
            rol_id = 1
            AND permiso_id = 1
    );

INSERT INTO
    seguridad.rol_permisos (rol_id, permiso_id, estado_id)
SELECT 1, 2, 1
WHERE
    NOT EXISTS (
        SELECT 1
        FROM seguridad.rol_permisos
        WHERE
            rol_id = 1
            AND permiso_id = 2
    );

INSERT INTO
    seguridad.rol_permisos (rol_id, permiso_id, estado_id)
SELECT 1, 3, 1
WHERE
    NOT EXISTS (
        SELECT 1
        FROM seguridad.rol_permisos
        WHERE
            rol_id = 1
            AND permiso_id = 3
    );

INSERT INTO
    seguridad.rol_permisos (rol_id, permiso_id, estado_id)
SELECT 1, 4, 1
WHERE
    NOT EXISTS (
        SELECT 1
        FROM seguridad.rol_permisos
        WHERE
            rol_id = 1
            AND permiso_id = 4
    );

INSERT INTO
    seguridad.rol_permisos (rol_id, permiso_id, estado_id)
SELECT 2, 1, 1
WHERE
    NOT EXISTS (
        SELECT 1
        FROM seguridad.rol_permisos
        WHERE
            rol_id = 2
            AND permiso_id = 1
    );

INSERT INTO
    seguridad.rol_permisos (rol_id, permiso_id, estado_id)
SELECT 2, 4, 1
WHERE
    NOT EXISTS (
        SELECT 1
        FROM seguridad.rol_permisos
        WHERE
            rol_id = 2
            AND permiso_id = 4
    );

INSERT INTO
    seguridad.rol_permisos (rol_id, permiso_id, estado_id)
SELECT 3, 1, 1
WHERE
    NOT EXISTS (
        SELECT 1
        FROM seguridad.rol_permisos
        WHERE
            rol_id = 3
            AND permiso_id = 1
    );

-- Insertar grupos de menú solo si no existen
INSERT INTO
    seguridad.menu_grupo (
        id,
        nombre,
        descripcion,
        icono,
        orden,
        nombre_despliegue,
        estado_id
    )
SELECT 1, 'Monitoreo', 'Módulos de monitoreo de red', 'monitor', 1, 'Monitoreo', 1
WHERE
    NOT EXISTS (
        SELECT 1
        FROM seguridad.menu_grupo
        WHERE
            id = 1
    );

INSERT INTO
    seguridad.menu_grupo (
        id,
        nombre,
        descripcion,
        icono,
        orden,
        nombre_despliegue,
        estado_id
    )
SELECT 2, 'Administración', 'Módulos administrativos', 'settings', 2, 'Administración', 1
WHERE
    NOT EXISTS (
        SELECT 1
        FROM seguridad.menu_grupo
        WHERE
            id = 2
    );

-- Insertar menús del sistema solo si no existen
INSERT INTO
    seguridad.menu (
        id,
        nombre,
        descripcion,
        url,
        icono,
        orden,
        nombre_despliegue,
        menu_grupo_id,
        estado_id
    )
SELECT 1, 'Interfaces', 'Tabla de interfaces de red', '/interfaces', 'table', 1, 'Interfaces', 1, 1
WHERE
    NOT EXISTS (
        SELECT 1
        FROM seguridad.menu
        WHERE
            id = 1
    );

INSERT INTO
    seguridad.menu (
        id,
        nombre,
        descripcion,
        url,
        icono,
        orden,
        nombre_despliegue,
        menu_grupo_id,
        estado_id
    )
SELECT 2, 'Topología', 'Mapa de topología de red', '/topologia', 'map', 2, 'Topología', 1, 1
WHERE
    NOT EXISTS (
        SELECT 1
        FROM seguridad.menu
        WHERE
            id = 2
    );

INSERT INTO
    seguridad.menu (
        id,
        nombre,
        descripcion,
        url,
        icono,
        orden,
        nombre_despliegue,
        menu_grupo_id,
        estado_id
    )
SELECT 3, 'Usuarios', 'Gestión de usuarios', '/usuarios', 'users', 1, 'Usuarios', 2, 1
WHERE
    NOT EXISTS (
        SELECT 1
        FROM seguridad.menu
        WHERE
            id = 3
    );

-- Asignar menús a roles solo si no existen
INSERT INTO
    seguridad.rol_menu (
        menu_id,
        rol_id,
        estado_tipo_id
    )
SELECT 1, 1, 1
WHERE
    NOT EXISTS (
        SELECT 1
        FROM seguridad.rol_menu
        WHERE
            menu_id = 1
            AND rol_id = 1
    );

INSERT INTO
    seguridad.rol_menu (
        menu_id,
        rol_id,
        estado_tipo_id
    )
SELECT 2, 1, 1
WHERE
    NOT EXISTS (
        SELECT 1
        FROM seguridad.rol_menu
        WHERE
            menu_id = 2
            AND rol_id = 1
    );

INSERT INTO
    seguridad.rol_menu (
        menu_id,
        rol_id,
        estado_tipo_id
    )
SELECT 3, 1, 1
WHERE
    NOT EXISTS (
        SELECT 1
        FROM seguridad.rol_menu
        WHERE
            menu_id = 3
            AND rol_id = 1
    );

INSERT INTO
    seguridad.rol_menu (
        menu_id,
        rol_id,
        estado_tipo_id
    )
SELECT 1, 2, 1
WHERE
    NOT EXISTS (
        SELECT 1
        FROM seguridad.rol_menu
        WHERE
            menu_id = 1
            AND rol_id = 2
    );

INSERT INTO
    seguridad.rol_menu (
        menu_id,
        rol_id,
        estado_tipo_id
    )
SELECT 2, 2, 1
WHERE
    NOT EXISTS (
        SELECT 1
        FROM seguridad.rol_menu
        WHERE
            menu_id = 2
            AND rol_id = 2
    );

INSERT INTO
    seguridad.rol_menu (
        menu_id,
        rol_id,
        estado_tipo_id
    )
SELECT 1, 3, 1
WHERE
    NOT EXISTS (
        SELECT 1
        FROM seguridad.rol_menu
        WHERE
            menu_id = 1
            AND rol_id = 3
    );

-- Crear usuario administrador por defecto solo si no existe (clave: admin123)
INSERT INTO
    seguridad.usuario (
        id,
        rol_id,
        email,
        nombre_usuario,
        clave_hash,
        estado_id,
        fecha_inicio
    )
SELECT 1, 1, 'admin@monitoreo.cl', 'Administrador', '$2b$12$LQv3c1yqBWVHxkd0L8k7OeY2J0VZ5X5Z5Z5Z5Z5Z5Z5Z5Z5Z5Z5Z', 1, NOW()
WHERE
    NOT EXISTS (
        SELECT 1
        FROM seguridad.usuario
        WHERE
            id = 1
    );