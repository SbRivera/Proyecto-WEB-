from pydantic import BaseModel, EmailStr, field_validator
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

    @field_validator('nombre_completo')
    def validate_nombre_completo(cls, value):
        if not all(x.isalpha() or x.isspace() for x in value) or value.strip().count(' ') < 1:
            raise ValueError('Nombre completo debe contener solo letras y al menos un espacio.')
        return value

    @field_validator('nombre_usuario')
    def validate_nombre_usuario(cls, value):
        if len(value) < 4:
            raise ValueError('Usuario debe tener al menos 4 caracteres.')
        return value

    @field_validator('contrasena')
    def validate_contrasena(cls, value):
        if len(value) < 4:
            raise ValueError('Contraseña debe tener al menos 4 caracteres.')
        return value

    @field_validator('cedula_identidad')
    def validate_cedula_identidad(cls, value):
        if not value.isdigit() or len(value) != 10:
            raise ValueError('Cédula de Identidad debe contener exactamente 10 números.')
        return value

    @field_validator('fecha_nacimiento')
    def validate_fecha_nacimiento(cls, value):
        birth_date = datetime.strptime(value, "%Y-%m-%d")
        if (datetime.now() - birth_date).days < 18 * 365:
            raise ValueError('Debe tener al menos 18 años.')
        return value

    @field_validator('contacto')
    def validate_contacto(cls, value):
        if value and (not value.isdigit() or len(value) != 10):
            raise ValueError('Contacto debe contener exactamente 10 números.')
        return value

    @field_validator('nacionalidad')
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

    @field_validator('contacto')
    def validate_contacto(cls, value):
        if value and (not value.isdigit() or len(value) != 10):
            raise ValueError('Contacto debe contener exactamente 10 números.')
        return value

class CheckUniqueRequest(BaseModel):
    field: str
    value: str

from pydantic import BaseModel, EmailStr
from typing import Optional

class UsuarioPublico(BaseModel):
    nombre_completo: str
    nombre_usuario: str
    correo_electronico: EmailStr
    cedula_identidad: str
    fecha_nacimiento: str  # Aquí declaramos que debe ser una cadena
    contacto: str
    nacionalidad: Optional[str] = None
    discapacidades: Optional[str] = None

    class Config:
        from_attributes = True

    @staticmethod
    def from_orm(obj):
        return UsuarioPublico(
            nombre_completo=obj.nombre_completo,
            nombre_usuario=obj.nombre_usuario,
            correo_electronico=obj.correo_electronico,
            cedula_identidad=obj.cedula_identidad,
            fecha_nacimiento=obj.fecha_nacimiento.strftime('%Y-%m-%d'),  # Convertimos a cadena
            contacto=obj.contacto,
            nacionalidad=obj.nacionalidad,
            discapacidades=obj.discapacidades
        )
    



