# backend/app/models/estado.py
from sqlalchemy import Column, Integer, String
from app.core.database import Base

class Estado(Base):
    __tablename__ = "estados"
    __table_args__ = {'schema': 'seguridad'}

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(String(250))