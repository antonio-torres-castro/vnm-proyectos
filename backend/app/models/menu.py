# backend/app/models/menu.py
from app.core.database import Base
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class MenuGrupo(Base):
    __tablename__ = "menu_grupo"
    __table_args__ = {"schema": "seguridad"}

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(150), nullable=False)
    descripcion = Column(String(300))
    icono = Column(String(50))
    orden = Column(Integer, default=0)
    nombre_despliegue = Column(String(150))
    estado_id = Column(Integer, ForeignKey("seguridad.estados.id"))
    fecha_creacion = Column(DateTime, default=func.now())
    fecha_modificacion = Column(DateTime, default=func.now(), onupdate=func.now())

    # Relaciones
    menus = relationship("Menu", back_populates="grupo")
    estado = relationship("Estado", back_populates="menu_grupos")


class Menu(Base):
    __tablename__ = "menu"
    __table_args__ = {"schema": "seguridad"}

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(150), nullable=False)
    descripcion = Column(String(300))
    url = Column(String(100))
    icono = Column(String(50))
    orden = Column(Integer, default=0)
    nombre_despliegue = Column(String(150))
    menu_grupo_id = Column(Integer, ForeignKey("seguridad.menu_grupo.id"))
    estado_id = Column(Integer, ForeignKey("seguridad.estados.id"))
    fecha_creacion = Column(DateTime, default=func.now())
    fecha_modificacion = Column(DateTime, default=func.now(), onupdate=func.now())

    # Relaciones
    grupo = relationship("MenuGrupo", back_populates="menus")
    estado = relationship("Estado", back_populates="menus")
    roles = relationship("RolMenu", back_populates="menu")
