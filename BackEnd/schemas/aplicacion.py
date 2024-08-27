from pydantic import BaseModel
from typing import List, Optional

class AplicacionBase(BaseModel):
    sitio_id: int
    contacto_emergencia: str
    fecha_visita: str
    tipo_visita: str
    estado: Optional[str] = None

class AplicacionCreate(AplicacionBase):
    participant_ids: List[str]

class AplicacionUpdate(BaseModel):
    grupo_id: str
    estado: str

class Aplicacion(AplicacionBase):
    id: int
    grupo_id: str
    participants: List[str]

    class Config:
        orm_mode = True
