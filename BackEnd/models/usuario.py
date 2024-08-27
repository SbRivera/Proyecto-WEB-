from sqlalchemy import Column, Integer, String, Date
from database import Base

class Usuario(Base):
    __tablename__ = 'usuarios'

    id = Column(Integer, primary_key=True, index=True)
    nombre_completo = Column(String, index=True)
    nombre_usuario = Column(String, unique=True, index=True)
    contrasena = Column(String)
    correo_electronico = Column(String, unique=True, index=True)
    cedula_identidad = Column(String, unique=True, index=True)
    fecha_nacimiento = Column(Date)
    contacto = Column(String)
    nacionalidad = Column(String, nullable=True)
    discapacidades = Column(String, nullable=True)
    nivel_acceso = Column(String, default='visitante')
