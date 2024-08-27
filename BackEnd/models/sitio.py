from sqlalchemy import Column, Integer, String, Boolean
from database import Base

class Sitio(Base):
    __tablename__ = "sitios"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, index=True)
    descripcion = Column(String)
    requisitos = Column(String)
    vestimenta = Column(String)
    restricciones = Column(String)
    disponibilidad = Column(String)
    activo = Column(Boolean, default=True)
