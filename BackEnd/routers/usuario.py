from fastapi import APIRouter, HTTPException
from models.usuario import UserRegister, UserLogin, UserUpdate, CheckUniqueRequest
from .database import get_db
import bcrypt
from psycopg2 import sql

router = APIRouter()

@router.post("/check_unique")
def check_unique(data: CheckUniqueRequest):
    query_map = {
        'nombre_usuario': "SELECT COUNT(*) FROM usuarios WHERE nombre_usuario = %s",
        'cedula_identidad': "SELECT COUNT(*) FROM usuarios WHERE cedula_identidad = %s",
    }

    if data.field not in query_map:
        raise HTTPException(status_code=400, detail="Campo inválido")

    with get_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query_map[data.field], (data.value,))
            count = cursor.fetchone()[0]
            return {"unique": count == 0}

@router.post("/register")
def register(usuario: UserRegister):
    with get_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM usuarios WHERE nombre_usuario = %s OR cedula_identidad = %s", (usuario.nombre_usuario, usuario.cedula_identidad))
            if cursor.fetchone()[0] > 0:
                raise HTTPException(status_code=400, detail="Nombre de usuario o cédula de identidad ya están en uso")

            hashed_password = bcrypt.hashpw(usuario.contrasena.encode('utf-8'), bcrypt.gensalt())
            query = sql.SQL("""
                INSERT INTO usuarios (nombre_completo, nombre_usuario, contrasena, nivel_acceso, correo_electronico, cedula_identidad, fecha_nacimiento, contacto, nacionalidad, discapacidades)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """)
            cursor.execute(query, (
                usuario.nombre_completo,
                usuario.nombre_usuario,
                hashed_password.decode('utf-8'),
                'visitante', 
                usuario.correo_electronico,
                usuario.cedula_identidad,
                usuario.fecha_nacimiento,
                usuario.contacto,
                usuario.nacionalidad,
                usuario.discapacidades
            ))
            conn.commit()
    return {"message": "Usuario registrado exitosamente"}

@router.post("/login")
def login(user: UserLogin):
    with get_db() as conn:
        with conn.cursor() as cursor:
            query = sql.SQL("SELECT contrasena, nivel_acceso FROM usuarios WHERE nombre_usuario = %s")
            cursor.execute(query, (user.nombre_usuario,))
            result = cursor.fetchone()
            if result is None or not bcrypt.checkpw(user.contrasena.encode('utf-8'), result[0].encode('utf-8')):
                raise HTTPException(status_code=401, detail="Invalid username or password")
            return {"message": "Login successful", "role": result[1]}

@router.get("/info/{nombre_usuario}")
def get_user_basic_info(nombre_usuario: str):
    with get_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT nombre_completo, cedula_identidad FROM usuarios WHERE nombre_usuario = %s", (nombre_usuario,))
            user_data = cursor.fetchone()
            if user_data:
                return {"full_name": user_data[0], "identity_card": user_data[1]}
            raise HTTPException(status_code=404, detail="User not found")

@router.get("/cedula/{cedula_identidad}")
def get_user_by_identity_card(cedula_identidad: str):
    with get_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT nombre_completo, cedula_identidad FROM usuarios WHERE cedula_identidad = %s", (cedula_identidad,))
            user_data = cursor.fetchone()
            if user_data:
                return {"full_name": user_data[0], "identity_card": user_data[1]}
            raise HTTPException(status_code=404, detail="User not found")

@router.get("/usuario/{nombre_usuario}")
def get_usuario(nombre_usuario: str):
    with get_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT nombre_usuario, correo_electronico, contacto, discapacidades FROM usuarios WHERE nombre_usuario = %s", (nombre_usuario,))
            usuario_data = cursor.fetchone()
            if usuario_data:
                return {"nombre_usuario": usuario_data[0], "correo_electronico": usuario_data[1], "contacto": usuario_data[2], "discapacidades": usuario_data[3]}
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

@router.put("/usuario/{nombre_usuario}")
def update_usuario(nombre_usuario: str, usuario: UserUpdate):
    with get_db() as conn:
        with conn.cursor() as cursor:
            if usuario.nombre_usuario and usuario.nombre_usuario != nombre_usuario:
                cursor.execute("SELECT COUNT(*) FROM usuarios WHERE nombre_usuario = %s", (usuario.nombre_usuario,))
                if cursor.fetchone()[0] > 0:
                    raise HTTPException(status_code=400, detail="El nombre de usuario ya existe")

            update_fields = []
            update_values = []
            if usuario.correo_electronico:
                update_fields.append("correo_electronico = %s")
                update_values.append(usuario.correo_electronico)
            if usuario.contacto:
                update_fields.append("contacto = %s")
                update_values.append(usuario.contacto)
            if usuario.discapacidades:
                update_fields.append("discapacidades = %s")
                update_values.append(usuario.discapacidades)
            if usuario.nombre_usuario:
                update_fields.append("nombre_usuario = %s")
                update_values.append(usuario.nombre_usuario)
            if usuario.contrasena:
                hashed_password = bcrypt.hashpw(usuario.contrasena.encode('utf-8'), bcrypt.gensalt())
                update_fields.append("contrasena = %s")
                update_values.append(hashed_password.decode('utf-8'))

            if update_fields:
                update_values.append(nombre_usuario)
                query = f"UPDATE usuarios SET {', '.join(update_fields)} WHERE nombre_usuario = %s"
                cursor.execute(query, tuple(update_values))
                conn.commit()
                
                if usuario.nombre_usuario:
                    return {"message": "Usuario actualizado exitosamente", "nuevo_nombre_usuario": usuario.nombre_usuario}

    return {"message": "Usuario actualizado exitosamente"}


