# backend/app/models/estado.py
from app.core.database import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship


class Estado(Base):
    __tablename__ = "estados"
    __table_args__ = {"schema": "seguridad"}

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(String(250))

    # Relaciones
    usuarios = relationship("Usuario", back_populates="estado")
    menus = relationship("Menu", back_populates="estado")
    menu_grupos = relationship("MenuGrupo", back_populates="estado")
    rol_permisos = relationship("RolPermiso", back_populates="estado")
    rol_menus = relationship("RolMenu", back_populates="estado")
    usuario_historias = relationship("UsuarioHistoria", back_populates="estado")
