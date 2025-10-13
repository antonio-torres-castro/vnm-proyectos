from app.core.database import Base
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class Usuario(Base):
    __tablename__ = "usuario"
    __table_args__ = {"schema": "seguridad"}

    id = Column(Integer, primary_key=True, index=True)
    rol_id = Column(Integer, ForeignKey("seguridad.rol.id"))
    email = Column(String(150), unique=True, nullable=False, index=True)
    nombre_usuario = Column(String(100), nullable=False)
    clave_hash = Column(String(255), nullable=False)
    fecha_creacion = Column(DateTime, default=func.now())
    fecha_inicio = Column(DateTime)
    fecha_termino = Column(DateTime)
    fecha_modificacion = Column(DateTime, default=func.now(), onupdate=func.now())
    estado_id = Column(Integer, ForeignKey("seguridad.estados.id"))

    # Relaciones
    rol = relationship("Rol", back_populates="usuarios")
    estado = relationship("Estado", back_populates="usuarios")
    historia = relationship(
        "UsuarioHistoria",
        back_populates="usuario",
        foreign_keys="UsuarioHistoria.usuario_id",
    )
