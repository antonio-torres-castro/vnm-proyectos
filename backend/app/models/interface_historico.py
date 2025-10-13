from app.core.database import Base
from sqlalchemy import (
    DECIMAL,
    TIMESTAMP,
    BigInteger,
    Column,
    DateTime,
    ForeignKey,
    Index,
    Integer,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class InterfaceHistorico(Base):
    __tablename__ = "interface_historico"
    __table_args__ = (
        Index("idx_interface_historico_devif", "devif"),
        Index("idx_interface_historico_timestamp", "timestamp"),
        Index("idx_interface_historico_devif_timestamp", "devif", "timestamp"),
        {"schema": "monitoreo"},
    )

    # Campos principales
    id = Column(Integer, primary_key=True, index=True)
    devif = Column(
        Integer,
        ForeignKey("monitoreo.interfaces.devif", ondelete="CASCADE"),
        nullable=False,
    )
    timestamp = Column(TIMESTAMP(timezone=True), nullable=False)

    # Métricas históricas de la interface
    input = Column(BigInteger)  # Data rate entrada (bps)
    output = Column(BigInteger)  # Data rate salida (bps)
    ifspeed = Column(Integer)  # Link Speed (Mbps)
    ifindis = Column(Integer)  # Descartes entrada (rate/s)
    ifoutdis = Column(Integer)  # Descartes salida (rate/s)
    ifinerr = Column(Integer)  # Errores entrada (rate/s)
    ifouterr = Column(Integer)  # Errores salida (rate/s)
    ifutil = Column(DECIMAL(5, 2))  # Utilización (%)

    # Timestamp de auditoría
    created_at = Column(DateTime, default=func.now())

    # Relaciones
    interface = relationship("Interfaces", back_populates="historico")

    def __repr__(self):
        return f"<InterfaceHistorico(id={self.id}, devif={self.devif}, timestamp={self.timestamp}, ifutil={self.ifutil})>"
