# backend/app/services/usuario_service.py
from typing import Optional, List
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_, and_
from app.models import Usuario, UsuarioHistoria, Rol, Estado
from app.schemas.usuario import UsuarioCreate, UsuarioUpdate, UsuarioChangePassword
from app.schemas.usuario_historia import UsuarioHistoriaCreate
from app.core.security import get_password_hash, verify_password
from datetime import datetime


class UsuarioService:

    @staticmethod
    def get_by_id(db: Session, usuario_id: int) -> Optional[Usuario]:
        """Obtener usuario por ID con relaciones cargadas"""
        return (
            db.query(Usuario)
            .options(joinedload(Usuario.rol), joinedload(Usuario.estado))
            .filter(Usuario.id == usuario_id)
            .first()
        )

    @staticmethod
    def get_by_email(db: Session, email: str) -> Optional[Usuario]:
        """Obtener usuario por email"""
        return db.query(Usuario).filter(Usuario.email == email).first()

    @staticmethod
    def get_all(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        search: Optional[str] = None,
        rol_id: Optional[int] = None,
        estado_id: Optional[int] = None,
    ) -> tuple[List[Usuario], int]:
        """Obtener usuarios con filtros y paginación"""
        query = db.query(Usuario).options(
            joinedload(Usuario.rol), joinedload(Usuario.estado)
        )

        # Aplicar filtros
        if search:
            query = query.filter(
                or_(
                    Usuario.email.ilike(f"%{search}%"),
                    Usuario.nombre_usuario.ilike(f"%{search}%"),
                )
            )

        if rol_id:
            query = query.filter(Usuario.rol_id == rol_id)

        if estado_id:
            query = query.filter(Usuario.estado_id == estado_id)

        total = query.count()
        usuarios = query.offset(skip).limit(limit).all()

        return usuarios, total

    @staticmethod
    def create(
        db: Session,
        usuario_data: UsuarioCreate,
        usuario_creador_id: Optional[int] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
    ) -> Usuario:
        """Crear nuevo usuario con auditoría"""

        # Verificar que el email no existe
        if UsuarioService.get_by_email(db, usuario_data.email):
            raise ValueError("El email ya existe en el sistema")

        # Crear hash de contraseña
        hashed_password = get_password_hash(usuario_data.clave)

        # Crear usuario
        db_usuario = Usuario(
            email=usuario_data.email,
            nombre_usuario=usuario_data.nombre_usuario,
            rol_id=usuario_data.rol_id,
            clave_hash=hashed_password,
            fecha_inicio=usuario_data.fecha_inicio,
            fecha_termino=usuario_data.fecha_termino,
            estado_id=usuario_data.estado_id or 1,
        )

        db.add(db_usuario)
        db.flush()  # Para obtener el ID

        # Crear registro de auditoría
        UsuarioService._create_historia(
            db=db,
            usuario=db_usuario,
            accion="CREATE",
            usuario_modificador_id=usuario_creador_id,
            ip_address=ip_address,
            user_agent=user_agent,
        )

        db.commit()
        db.refresh(db_usuario)
        return db_usuario

    @staticmethod
    def update(
        db: Session,
        usuario_id: int,
        usuario_data: UsuarioUpdate,
        usuario_modificador_id: Optional[int] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
    ) -> Optional[Usuario]:
        """Actualizar usuario con auditoría"""

        db_usuario = UsuarioService.get_by_id(db, usuario_id)
        if not db_usuario:
            return None

        # Guardar estado anterior para auditoría
        usuario_anterior = Usuario(
            id=db_usuario.id,
            email=db_usuario.email,
            nombre_usuario=db_usuario.nombre_usuario,
            rol_id=db_usuario.rol_id,
            clave_hash=db_usuario.clave_hash,
            estado_id=db_usuario.estado_id,
        )

        # Verificar email único si se está cambiando
        if usuario_data.email and usuario_data.email != db_usuario.email:
            if UsuarioService.get_by_email(db, usuario_data.email):
                raise ValueError("El email ya existe en el sistema")

        # Actualizar campos
        update_data = usuario_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_usuario, field, value)

        db_usuario.fecha_modificacion = datetime.utcnow()

        # Crear registro de auditoría
        UsuarioService._create_historia(
            db=db,
            usuario=usuario_anterior,  # Estado anterior
            accion="UPDATE",
            usuario_modificador_id=usuario_modificador_id,
            ip_address=ip_address,
            user_agent=user_agent,
        )

        db.commit()
        db.refresh(db_usuario)
        return db_usuario

    @staticmethod
    def change_password(
        db: Session,
        usuario_id: int,
        password_data: UsuarioChangePassword,
        usuario_modificador_id: Optional[int] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
    ) -> bool:
        """Cambiar contraseña de usuario"""

        db_usuario = UsuarioService.get_by_id(db, usuario_id)
        if not db_usuario:
            return False

        # Verificar contraseña actual
        if not verify_password(password_data.clave_actual, db_usuario.clave_hash):
            raise ValueError("Contraseña actual incorrecta")

        # Actualizar contraseña
        db_usuario.clave_hash = get_password_hash(password_data.clave_nueva)
        db_usuario.fecha_modificacion = datetime.utcnow()

        # Crear registro de auditoría (sin incluir hash de contraseña)
        UsuarioService._create_historia(
            db=db,
            usuario=db_usuario,
            accion="CHANGE_PASSWORD",
            usuario_modificador_id=usuario_modificador_id,
            ip_address=ip_address,
            user_agent=user_agent,
            include_password=False,
        )

        db.commit()
        return True

    @staticmethod
    def deactivate(
        db: Session,
        usuario_id: int,
        usuario_modificador_id: Optional[int] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
    ) -> bool:
        """Desactivar usuario (cambiar estado a inactivo)"""

        db_usuario = UsuarioService.get_by_id(db, usuario_id)
        if not db_usuario:
            return False

        # Cambiar estado a inactivo (asumiendo que 2 = inactivo)
        db_usuario.estado_id = 2
        db_usuario.fecha_modificacion = datetime.utcnow()

        # Crear registro de auditoría
        UsuarioService._create_historia(
            db=db,
            usuario=db_usuario,
            accion="DEACTIVATE",
            usuario_modificador_id=usuario_modificador_id,
            ip_address=ip_address,
            user_agent=user_agent,
        )

        db.commit()
        return True

    @staticmethod
    def get_historia(
        db: Session, usuario_id: Optional[int] = None, skip: int = 0, limit: int = 100
    ) -> tuple[List[UsuarioHistoria], int]:
        """Obtener historial de auditoría de usuarios"""

        query = db.query(UsuarioHistoria).options(
            joinedload(UsuarioHistoria.usuario),
            joinedload(UsuarioHistoria.rol),
            joinedload(UsuarioHistoria.estado),
            joinedload(UsuarioHistoria.usuario_modificador),
        )

        if usuario_id:
            query = query.filter(UsuarioHistoria.usuario_id == usuario_id)

        query = query.order_by(UsuarioHistoria.fecha.desc())

        total = query.count()
        historia = query.offset(skip).limit(limit).all()

        return historia, total

    @staticmethod
    def _create_historia(
        db: Session,
        usuario: Usuario,
        accion: str,
        usuario_modificador_id: Optional[int] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
        include_password: bool = False,
    ):
        """Crear registro de auditoría en usuario_historia"""

        historia = UsuarioHistoria(
            usuario_id=usuario.id,
            rol_id=usuario.rol_id,
            email=usuario.email,
            nombre_usuario=usuario.nombre_usuario,
            clave_hash=usuario.clave_hash if include_password else None,
            estado_id=usuario.estado_id,
            accion=accion,
            usuario_modificador_id=usuario_modificador_id,
            ip_address=ip_address,
            user_agent=user_agent,
        )

        db.add(historia)
