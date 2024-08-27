from pydantic import BaseModel

class SitioBase(BaseModel):
    titulo: str
    descripcion: str
    requisitos: str
    vestimenta: str
    restricciones: str
    disponibilidad: int
    activo: bool

class SitioCreate(SitioBase):
    pass

class Sitio(SitioBase):
    id: int

    class Config:
        orm_mode = True
