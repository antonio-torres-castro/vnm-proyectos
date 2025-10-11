# backend/app/models/menu.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.core.database import Base

class MenuGrupo(Base):
    __tablename__ = "menu_grupo"
    __table_args__ = {'schema': 'seguridad'}

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(150), nullable=False)
    descripcion = Column(String(300))
    icono = Column(String(50))
    orden = Column(Integer, default=0)
    nombre_despliegue = Column(String(150))
    estado_id = Column(Integer, ForeignKey('seguridad.estados.id'))
    fecha_creacion = Column(DateTime, default=func.now())
    fecha_modificacion = Column(DateTime, default=func.now(), onupdate=func.now())

class Menu(Base):
    __tablename__ = "menu"
    __table_args__ = {'schema': 'seguridad'}

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(150), nullable=False)
    descripcion = Column(String(300))
    url = Column(String(100))
    icono = Column(String(50))
    orden = Column(Integer, default=0)
    nombre_despliegue = Column(String(150))
    menu_grupo_id = Column(Integer, ForeignKey('seguridad.menu_grupo.id'))
    estado_id = Column(Integer, ForeignKey('seguridad.estados.id'))
    fecha_creacion = Column(DateTime, default=func.now())
    fecha_modificacion = Column(DateTime, default=func.now(), onupdate=func.now())