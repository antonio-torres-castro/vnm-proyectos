from sqlalchemy import Column, Integer, DateTime, DECIMAL, TIMESTAMP, ForeignKey, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class DispositivoHistorico(Base):
    __tablename__ = "dispositivo_historico"
    __table_args__ = (
        Index('idx_dispositivo_historico_devid', 'devid'),
        Index('idx_dispositivo_historico_timestamp', 'timestamp'),
        {'schema': 'monitoreo'}
    )

    # Campos principales
    id = Column(Integer, primary_key=True, index=True)
    devid = Column(Integer, ForeignKey('monitoreo.dispositivos.devid', ondelete='CASCADE'), nullable=False)
    timestamp = Column(TIMESTAMP(timezone=True), nullable=False)
    
    # Datos históricos del dispositivo
    devstatus = Column(Integer)  # Estado del dispositivo en este timestamp
    latitud = Column(DECIMAL(10, 8))    # Geolocalización histórica
    longitud = Column(DECIMAL(11, 8))   # Geolocalización histórica
    
    # Timestamp de auditoría
    created_at = Column(DateTime, default=func.now())

    # Relaciones
    dispositivo = relationship("Dispositivos", back_populates="historico")

    def __repr__(self):
        return f"<DispositivoHistorico(id={self.id}, devid={self.devid}, timestamp={self.timestamp}, devstatus={self.devstatus})>"
