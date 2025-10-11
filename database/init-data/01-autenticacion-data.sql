-- Datos iniciales para el sistema de autenticación y autorización
-- Este script se ejecuta automáticamente al iniciar los servicios

-- Insertar estados básicos del sistema
INSERT INTO
    seguridad.estados (id, nombre, descripcion)
VALUES (
        1,
        'Activo',
        'Registro activo en el sistema'
    ),
    (
        2,
        'Inactivo',
        'Registro inactivo en el sistema'
    ),
    (
        3,
        'Eliminado',
        'Registro marcado como eliminado'
    ),
    (
        4,
        'Pendiente',
        'Registro en estado pendiente'
    ),
    (
        5,
        'Aprobado',
        'Registro aprobado'
    ),
    (
        6,
        'Rechazado',
        'Registro rechazado'
    ) ON CONFLICT (id) DO NOTHING;

-- Insertar roles del sistema
INSERT INTO
    seguridad.rol (id, nombre, descripcion)
VALUES (
        1,
        'Administrador',
        'Acceso completo al sistema'
    ),
    (
        2,
        'Supervisor',
        'Acceso de supervisión y reportes'
    ),
    (
        3,
        'Ejecutor',
        'Acceso básico de ejecución'
    ) ON CONFLICT (id) DO NOTHING;

-- Insertar permisos del sistema
INSERT INTO
    seguridad.permisos (id, nombre, descripcion)
VALUES (
        1,
        'Lectura',
        'Permiso de lectura de datos'
    ),
    (
        2,
        'Creación',
        'Permiso de creación de registros'
    ),
    (
        3,
        'Modificación',
        'Permiso de modificación de registros'
    ),
    (
        4,
        'Exportación',
        'Permiso de exportación de datos'
    ) ON CONFLICT (id) DO NOTHING;

-- Asignar permisos a roles (Administrador tiene todos)
INSERT INTO
    seguridad.rol_permisos (rol_id, permiso_id, estado_id)
VALUES (1, 1, 1),
    (1, 2, 1),
    (1, 3, 1),
    (1, 4, 1),
    (2, 1, 1),
    (2, 4, 1),
    (3, 1, 1) ON CONFLICT (rol_id, permiso_id) DO NOTHING;

-- Insertar grupos de menú
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
VALUES (
        1,
        'Monitoreo',
        'Módulos de monitoreo de red',
        'monitor',
        1,
        'Monitoreo',
        1
    ),
    (
        2,
        'Administración',
        'Módulos administrativos',
        'settings',
        2,
        'Administración',
        1
    ) ON CONFLICT (id) DO NOTHING;

-- Insertar menús del sistema
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
VALUES (
        1,
        'Interfaces',
        'Tabla de interfaces de red',
        '/interfaces',
        'table',
        1,
        'Interfaces',
        1,
        1
    ),
    (
        2,
        'Topología',
        'Mapa de topología de red',
        '/topologia',
        'map',
        2,
        'Topología',
        1,
        1
    ),
    (
        3,
        'Usuarios',
        'Gestión de usuarios del sistema',
        '/usuarios',
        'users',
        1,
        'Usuarios',
        2,
        1
    ) ON CONFLICT (id) DO NOTHING;

-- Asignar menús a roles
INSERT INTO
    seguridad.rol_menu (
        menu_id,
        rol_id,
        estado_tipo_id
    )
VALUES (1, 1, 1),
    (2, 1, 1),
    (3, 1, 1),
    (1, 2, 1),
    (2, 2, 1),
    (1, 3, 1) ON CONFLICT (menu_id, rol_id) DO NOTHING;

-- Crear usuario administrador por defecto (clave: admin123)
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
VALUES (
        1,
        1,
        'admin@monitoreo.cl',
        'Administrador',
        '$2b$12$LQv3c1yqBWVHxkd0L8k7OeY2J0VZ5X5Z5Z5Z5Z5Z5Z5Z5Z5Z5Z5Z',
        1,
        NOW()
    ) ON CONFLICT (id) DO NOTHING;

-- Mensaje de confirmación
DO $$ 
BEGIN
    RAISE NOTICE '✅ Datos de autenticación inicializados correctamente';
END $$;