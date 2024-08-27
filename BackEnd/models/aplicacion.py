from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from database import Base

class Aplicacion(Base):
    __tablename__ = 'aplicaciones'

    id = Column(Integer, primary_key=True, index=True)
    sitio_id = Column(Integer, ForeignKey('sitios.id'))
    participante_id = Column(String, ForeignKey('usuarios.cedula_identidad'))
    contacto_emergencia = Column(String)
    fecha_visita = Column(Date)
    tipo_visita = Column(String)
    grupo_id = Column(UUID(as_uuid=True), default=uuid.uuid4, index=True) 
    estado = Column(String, nullable=True)

    sitio = relationship("Sitio")
    participante = relationship("Usuario")
