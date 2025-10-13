# backend/app/models/rol_menu.py
from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class RolMenu(Base):
    __tablename__ = "rol_menu"
    __table_args__ = {"schema": "seguridad"}

    menu_id = Column(Integer, ForeignKey("seguridad.menu.id"), primary_key=True)
    rol_id = Column(Integer, ForeignKey("seguridad.rol.id"), primary_key=True)
    estado_id = Column(Integer, ForeignKey("seguridad.estados.id"))
    fecha_creacion = Column(DateTime, default=func.now())
    fecha_modificacion = Column(DateTime, default=func.now(), onupdate=func.now())

    # Relaciones
    rol = relationship("Rol", back_populates="menus")
    menu = relationship("Menu", back_populates="roles")
    estado = relationship("Estado", back_populates="rol_menus")
