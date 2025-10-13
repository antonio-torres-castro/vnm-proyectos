# backend/app/models/usuario_historia.py
from app.core.database import Base
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class UsuarioHistoria(Base):
    __tablename__ = "usuario_historia"
    __table_args__ = {"schema": "seguridad"}

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("seguridad.usuario.id"), nullable=False)
    rol_id = Column(Integer, ForeignKey("seguridad.rol.id"))
    email = Column(String(150), nullable=False)
    nombre_usuario = Column(String(100), nullable=False)
    clave_hash = Column(String(255))
    estado_id = Column(Integer, ForeignKey("seguridad.estados.id"))
    fecha = Column(DateTime, default=func.now(), nullable=False)

    # Campos adicionales para auditoría
    accion = Column(String(50), nullable=False)  # CREATE, UPDATE, DELETE
    usuario_modificador_id = Column(Integer, ForeignKey("seguridad.usuario.id"))
    ip_address = Column(String(45))  # IPv4 o IPv6
    user_agent = Column(String(500))

    # Relaciones
    usuario = relationship(
        "Usuario", back_populates="historia", foreign_keys=[usuario_id]
    )
    rol = relationship("Rol", back_populates="usuario_historias")
    estado = relationship("Estado", back_populates="usuario_historias")
    usuario_modificador = relationship("Usuario", foreign_keys=[usuario_modificador_id])
