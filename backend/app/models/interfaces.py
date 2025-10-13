from app.core.database import Base
from sqlalchemy import (
    DECIMAL,
    TIMESTAMP,
    BigInteger,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class Interfaces(Base):
    __tablename__ = "interfaces"
    __table_args__ = (
        UniqueConstraint("devid", "devif", name="idx_interfaces_devif_unique"),
        {"schema": "monitoreo"},
    )

    # Campos principales
    id = Column(Integer, primary_key=True, index=True)
    devid = Column(
        Integer,
        ForeignKey("monitoreo.dispositivos.devid", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    devif = Column(Integer, nullable=False)  # ID de interface en JIPAM

    # Información de la interface
    ifname = Column(String(100))
    ifalias = Column(String(255))

    # Estados de la interface
    ifadmin = Column(Integer)  # 1:Up, >1:Down
    ifoper = Column(Integer)  # 1:Up, >1:Down
    ifstatus = Column(Integer, index=True)  # 1:UP(1,1), 2:Down(1,>1), 3:Shutdown(2,>1)
    iflv = Column(TIMESTAMP(timezone=True))  # Última vez que se vio
    iflc = Column(TIMESTAMP(timezone=True))  # Último cambio de estado
    ifgraficar = Column(Integer, index=True)  # 0:No monitoreo, 1:En monitoreo

    # Métricas de la interface (última muestra)
    time = Column(TIMESTAMP(timezone=True))  # Fecha/hora última muestra
    input = Column(BigInteger)  # Data rate entrada (bps)
    output = Column(BigInteger)  # Data rate salida (bps)
    ifspeed = Column(Integer)  # Link Speed (Mbps)
    ifindis = Column(Integer)  # Descartes entrada (rate/s)
    ifoutdis = Column(Integer)  # Descartes salida (rate/s)
    ifinerr = Column(Integer)  # Errores entrada (rate/s)
    ifouterr = Column(Integer)  # Errores salida (rate/s)
    ifutil = Column(DECIMAL(5, 2))  # Utilización (%)

    # Timestamps de auditoría
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # Relaciones
    dispositivo = relationship("Dispositivos", back_populates="interfaces")
    historico = relationship(
        "InterfaceHistorico", back_populates="interface", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Interfaces(id={self.id}, devid={self.devid}, devif={self.devif}, ifname='{self.ifname}', ifstatus={self.ifstatus})>"
