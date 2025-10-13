# backend/app/models/rol.py
from app.core.database import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship


class Rol(Base):
    __tablename__ = "rol"
    __table_args__ = {"schema": "seguridad"}

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(String(250))

    # Relaciones
    usuarios = relationship("Usuario", back_populates="rol")
    permisos = relationship("RolPermiso", back_populates="rol")
    menus = relationship("RolMenu", back_populates="rol")
    usuario_historias = relationship("UsuarioHistoria", back_populates="rol")
