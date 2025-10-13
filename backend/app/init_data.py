# backend/app/init_data.py
"""
Script para inicializar datos básicos del sistema
IMPORTANTE: Las tablas primitivas (estados, permisos, rol) se poblan únicamente
por scripts SQL directos y no deben poblarse desde código si ya tienen registros.
"""

from sqlalchemy.orm import Session
from app.core.database import SessionLocal, engine, Base
from app.models import Estado, Rol, Usuario, Permiso
from app.models import *  # Importar todos los modelos para crear tablas
from app.core.security import get_password_hash
from datetime import datetime
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def check_primitive_tables_empty(db: Session) -> bool:
    """
    Verificar que las tablas primitivas estén vacías.
    Las tablas primitivas (estados, permisos, rol) se poblan únicamente por scripts SQL.
    """
    try:
        # Verificar tabla estados
        estado_count = db.query(Estado).count()
        if estado_count > 0:
            logger.info(f"Tabla estados ya contiene {estado_count} registros - poblada por script SQL")
            return False
        
        # Verificar tabla permisos
        permiso_count = db.query(Permiso).count()
        if permiso_count > 0:
            logger.info(f"Tabla permisos ya contiene {permiso_count} registros - poblada por script SQL")
            return False
        
        # Verificar tabla rol
        rol_count = db.query(Rol).count()
        if rol_count > 0:
            logger.info(f"Tabla rol ya contiene {rol_count} registros - poblada por script SQL")
            return False
        
        logger.info("Tablas primitivas están vacías - se pueden poblar")
        return True
        
    except Exception as e:
        logger.error(f"Error verificando tablas primitivas: {e}")
        return False

def init_estados(db: Session):
    """
    Inicializar estados básicos del sistema.
    SOLO si la tabla está completamente vacía.
    """
    # Verificar que la tabla esté vacía
    if db.query(Estado).count() > 0:
        logger.warning("Tabla estados ya contiene registros - no se puede poblar desde código")
        return
    #creado, activo, inactivo, eliminado, iniciado, terminado, rechazado, aprobado
    estados_basicos = [
        {"id": 1, "nombre": "Creado", "descripcion": "Registro creado en el sistema"},
        {"id": 2, "nombre": "Activo", "descripcion": "Registro activo en el sistema"},
        {"id": 3, "nombre": "Inactivo", "descripcion": "Registro inactivo en el sistema"},
        {"id": 4, "nombre": "Eliminado", "descripcion": "Registro eliminado logicamente en el sistema"},
        {"id": 5, "nombre": "Iniciado", "descripcion": "Proceso o Vigencia en ambito del modulo respectivo a iniciado"},
        {"id": 6, "nombre": "Terminado", "descripcion": "Proceso o Vigencia en ambito del modulo respectivo a terminado"},
        {"id": 7, "nombre": "Rechazado", "descripcion": "Proceso o Tarea en ambito del modulo respectivo rechazada"},
        {"id": 8, "nombre": "Aprobado", "descripcion": "Proceso o Tarea en ambito del modulo respectivo aprobada"}
    ]
    
    for estado_data in estados_basicos:
        estado = Estado(
            id=estado_data["id"],
            nombre=estado_data["nombre"],
            descripcion=estado_data["descripcion"]
        )
        db.add(estado)
        logger.info(f"Estado creado: {estado_data['nombre']}")

def init_roles(db: Session):
    """
    Inicializar roles básicos del sistema.
    SOLO si la tabla está completamente vacía.
    """
    # Verificar que la tabla esté vacía
    if db.query(Rol).count() > 0:
        logger.warning("Tabla rol ya contiene registros - no se puede poblar desde código")
        return
    
    roles_basicos = [
        {"id": 1, "nombre": "Administrador", "descripcion": "Administrador del sistema con todos los permisos"},
        {"id": 2, "nombre": "Supervisor", "descripcion": "Supervisor con permisos limitados"},
        {"id": 3, "nombre": "Ejecutor", "descripcion": "Ejecutor básico con permisos de solo lectura"},
    ]
    
    for rol_data in roles_basicos:
        rol = Rol(
            id=rol_data["id"],
            nombre=rol_data["nombre"],
            descripcion=rol_data["descripcion"]
        )
        db.add(rol)
        logger.info(f"Rol creado: {rol_data['nombre']}")

def init_permisos(db: Session):
    """
    Inicializar permisos básicos del sistema.
    SOLO si la tabla está completamente vacía.
    """
    # Verificar que la tabla esté vacía
    if db.query(Permiso).count() > 0:
        logger.warning("Tabla permisos ya contiene registros - no se puede poblar desde código")
        return
    
    logger.info("Tabla permisos vacía - debe ser poblada por script SQL directo")

def init_admin_user(db: Session):
    """
    Crear usuario administrador por defecto.
    Esta función se ejecuta independientemente del estado de las tablas primitivas.
    """
    admin_email = "admin@monitoreo.cl"
    admin_usuario = "Administrador"
    admin_password = "admin123"
    
    # Verificar si ya existe
    usuario_existente = db.query(Usuario).filter(Usuario.email == admin_email).first()
    if usuario_existente:
        logger.info(f"Usuario administrador ya existe: {admin_email}")
        return
    
    # Verificar que existan los requisitos previos
    rol_admin = db.query(Rol).filter(Rol.id == 1).first()
    estado_activo = db.query(Estado).filter(Estado.id == 1).first()
    
    if not rol_admin:
        logger.error("No se puede crear usuario administrador: rol con ID 1 no existe")
        return
    
    if not estado_activo:
        logger.error("No se puede crear usuario administrador: estado con ID 1 no existe")
        return
    
    # Crear usuario administrador
    hashed_password = get_password_hash(admin_password)
    admin_user = Usuario(
        email=admin_email,
        nombre_usuario=admin_usuario,
        rol_id=1,  # Rol Administrador
        clave_hash=hashed_password,
        fecha_inicio=datetime.utcnow(),
        fecha_termino=None,
        estado_id=1,  # Estado Activo
        fecha_creacion=datetime.utcnow(),
        fecha_modificacion=datetime.utcnow()
    )
    
    db.add(admin_user)
    logger.info(f"Usuario administrador creado: {admin_email}")
    logger.info(f"Nombre de usuario: {admin_usuario}")
    logger.info(f"Contraseña: {admin_password}")

def init_database():
    """
    Función principal para inicializar la base de datos.
    
    IMPORTANTE: Las tablas primitivas (estados, permisos, rol) solo se poblan
    si están completamente vacías. Si ya tienen registros, significa que fueron
    pobladas por scripts SQL directos y no se deben modificar.
    """
    logger.info("Iniciando inicialización de la base de datos...")
    
    # Crear todas las tablas
    Base.metadata.create_all(bind=engine)
    
    # Crear sesión
    db = SessionLocal()
    
    try:
        # Verificar estado de tablas primitivas
        primitives_empty = check_primitive_tables_empty(db)
        
        if primitives_empty:
            logger.info("Tablas primitivas vacías - procediendo con inicialización desde código")
            # Inicializar datos básicos solo si las tablas están vacías
            init_estados(db)
            init_permisos(db)
            init_roles(db)
        else:
            logger.info("Tablas primitivas ya pobladas por scripts SQL - omitiendo inicialización desde código")
        
        # El usuario administrador se puede crear independientemente
        # siempre que existan los roles y estados requeridos
        init_admin_user(db)
        
        # Confirmar cambios
        db.commit()
        logger.info("Inicialización completada exitosamente")
        
    except Exception as e:
        logger.error(f"Error durante la inicialización: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    init_database()