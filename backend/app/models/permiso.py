# backend/app/models/permiso.py
from sqlalchemy import Column, Integer, String
from app.core.database import Base

class Permiso(Base):
    __tablename__ = "permisos"
    __table_args__ = {'schema': 'seguridad'}

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(String(250))