# backend/app/models/rol_permiso.py
from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class RolPermiso(Base):
    __tablename__ = "rol_permisos"
    __table_args__ = {"schema": "seguridad"}

    permiso_id = Column(Integer, ForeignKey("seguridad.permisos.id"), primary_key=True)
    rol_id = Column(Integer, ForeignKey("seguridad.rol.id"), primary_key=True)
    fecha_creacion = Column(DateTime, default=func.now())
    fecha_modificacion = Column(DateTime, default=func.now(), onupdate=func.now())
    estado_id = Column(Integer, ForeignKey("seguridad.estados.id"))

    # Relaciones
    rol = relationship("Rol", back_populates="permisos")
    permiso = relationship("Permiso", back_populates="roles")
    estado = relationship("Estado", back_populates="rol_permisos")
