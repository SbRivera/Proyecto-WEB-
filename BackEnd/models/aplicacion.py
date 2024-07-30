from pydantic import BaseModel
from typing import List, Optional

class Application(BaseModel):
    sitio_id: int
    participant_ids: List[str]
    contacto_emergencia: str
    fecha_visita: str
    tipo_visita: str
    estado: Optional[str] = None

class AplicacionUpdate(BaseModel):
    grupo_id: str
    estado: str
