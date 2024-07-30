from pydantic import BaseModel

class Site(BaseModel):
    titulo: str
    descripcion: str
    requisitos: str
    vestimenta: str
    restricciones: str
    disponibilidad: str
    activo: bool
