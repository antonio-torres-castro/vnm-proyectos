from sqlalchemy import Column, Integer, String, DateTime, DECIMAL, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import INET
from app.core.database import Base

class Dispositivos(Base):
    __tablename__ = "dispositivos"
    __table_args__ = {'schema': 'monitoreo'}

    # Campos principales
    devid = Column(Integer, primary_key=True, index=True)
    operador = Column(String(50))
    zona = Column(String(50), index=True)
    hub = Column(String(50), index=True)
    devip = Column(INET)
    area = Column(String(50), index=True)
    devname = Column(String(150))
    
    # Estados del dispositivo
    devstatus = Column(Integer, index=True)  # 0:No responde, 1:UP, 2:Caído, 5:Fuera de monitoreo
    devstatus_lv = Column(TIMESTAMP(timezone=True))  # Última vez que se vio
    devstatus_lc = Column(TIMESTAMP(timezone=True))  # Último cambio de estado
    
    # Información del dispositivo
    enterprise = Column(String(100), index=True)  # Fabricante
    modelo = Column(String(100))
    
    # Geolocalización
    latitud = Column(DECIMAL(10, 8))
    longitud = Column(DECIMAL(11, 8))
    
    # Timestamps de auditoría
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # Relaciones
    interfaces = relationship("Interfaces", back_populates="dispositivo", cascade="all, delete-orphan")
    historico = relationship("DispositivoHistorico", back_populates="dispositivo", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Dispositivos(devid={self.devid}, devname='{self.devname}', devstatus={self.devstatus})>"
