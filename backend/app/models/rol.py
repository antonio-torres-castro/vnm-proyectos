# backend/app/models/rol.py
from sqlalchemy import Column, Integer, String
from app.core.database import Base

class Rol(Base):
    __tablename__ = "rol"
    __table_args__ = {'schema': 'seguridad'}

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(String(250))