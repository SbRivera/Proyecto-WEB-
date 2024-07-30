from pydantic import BaseModel, EmailStr, validator
from typing import Optional
from datetime import datetime

class UserRegister(BaseModel):
    nombre_completo: str
    nombre_usuario: str
    contrasena: str
    correo_electronico: EmailStr
    cedula_identidad: str
    fecha_nacimiento: str
    contacto: str
    nacionalidad: Optional[str] = None
    discapacidades: Optional[str] = None

    @validator('nombre_completo')
    def validate_nombre_completo(cls, value):
        if not all(x.isalpha() or x.isspace() for x in value) or value.strip().count(' ') < 1:
            raise ValueError('Nombre completo debe contener solo letras y al menos un espacio.')
        return value

    @validator('nombre_usuario')
    def validate_nombre_usuario(cls, value):
        if len(value) < 4:
            raise ValueError('Usuario debe tener al menos 4 caracteres.')
        return value

    @validator('contrasena')
    def validate_contrasena(cls, value):
        if len(value) < 4:
            raise ValueError('Contraseña debe tener al menos 4 caracteres.')
        return value

    @validator('cedula_identidad')
    def validate_cedula_identidad(cls, value):
        if not value.isdigit() or len(value) != 10:
            raise ValueError('Cédula de Identidad debe contener exactamente 10 números.')
        return value

    @validator('fecha_nacimiento')
    def validate_fecha_nacimiento(cls, value):
        birth_date = datetime.strptime(value, "%Y-%m-%d")
        if (datetime.now() - birth_date).days < 18 * 365:
            raise ValueError('Debe tener al menos 18 años.')
        return value

    @validator('contacto')
    def validate_contacto(cls, value):
        if value and (not value.isdigit() or len(value) != 10):
            raise ValueError('Contacto debe contener exactamente 10 números.')
        return value

    @validator('nacionalidad')
    def validate_nacionalidad(cls, value):
        if value and not all(x.isalpha() or x.isspace() for x in value):
            raise ValueError('Nacionalidad debe contener solo letras y espacios.')
        return value

class UserLogin(BaseModel):
    nombre_usuario: str
    contrasena: str

class UserUpdate(BaseModel):
    correo_electronico: EmailStr
    contacto: str
    discapacidades: Optional[str] = None
    nombre_usuario: Optional[str] = None
    contrasena: Optional[str] = None

    @validator('contacto')
    def validate_contacto(cls, value):
        if value and (not value.isdigit() or len(value) != 10):
            raise ValueError('Contacto debe contener exactamente 10 números.')
        return value

class CheckUniqueRequest(BaseModel):
    field: str
    value: str
