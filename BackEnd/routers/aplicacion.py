from fastapi import APIRouter, HTTPException
from models.aplicacion import Application, AplicacionUpdate
from .database import get_db
from psycopg2 import sql
import uuid
from datetime import datetime


router = APIRouter()

@router.post("/aplicaciones")
def create_application(application: Application):
    grupo_id = str(uuid.uuid4())
    with get_db() as conn:
        with conn.cursor() as cursor:
            for participant_id in application.participant_ids:
                query = sql.SQL("""
                    INSERT INTO aplicaciones (sitio_id, participante_id, contacto_emergencia, fecha_visita, tipo_visita, grupo_id, estado)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """)
                cursor.execute(query, (
                    application.sitio_id,
                    participant_id,
                    application.contacto_emergencia,
                    application.fecha_visita,
                    application.tipo_visita,
                    grupo_id,
                    None
                ))
            conn.commit()
    return {"message": "Solicitud enviada exitosamente", "grupo_id": grupo_id}

@router.get("/aplicaciones")
def get_applications():
    with get_db() as conn:
        with conn.cursor() as cursor:
            query = """
                SELECT 
                    a.id, a.sitio_id, s.titulo as nombre_sitio, a.participante_id, 
                    a.contacto_emergencia, a.fecha_visita, a.tipo_visita, 
                    a.grupo_id, a.estado
                FROM aplicaciones a
                JOIN sitios s ON a.sitio_id = s.id
                WHERE a.fecha_visita >= %s
            """
            cursor.execute(query, (datetime.now().strftime('%Y-%m-%d'),))
            applications = cursor.fetchall()
            
            grouped_applications = {}
            for app in applications:
                grupo_id = app[7]
                if grupo_id not in grouped_applications:
                    grouped_applications[grupo_id] = {
                        "id": app[0],
                        "sitio_id": app[1],
                        "nombre_sitio": app[2],
                        "contacto_emergencia": app[4],
                        "fecha_visita": app[5],
                        "tipo_visita": app[6],
                        "grupo_id": app[7],
                        "estado": app[8],
                        "participants": []
                    }
                grouped_applications[grupo_id]["participants"].append(app[3])
                
            return list(grouped_applications.values())

@router.put("/aplicaciones/estado")
def update_application_status(update: AplicacionUpdate):
    with get_db() as conn:
        with conn.cursor() as cursor:
            query = "UPDATE aplicaciones SET estado = %s WHERE grupo_id = %s"
            cursor.execute(query, (update.estado, update.grupo_id))
            conn.commit()
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Solicitud no encontrada")
    return {"message": "Estado de la solicitud actualizado exitosamente"}


@router.get("/aplicaciones/{nombre_usuario}")
def get_user_applications(nombre_usuario: str):
    with get_db() as conn:
        with conn.cursor() as cursor:
            query = """
                SELECT 
                    a.id, a.sitio_id, s.titulo as nombre_sitio, a.participante_id, 
                    a.contacto_emergencia, a.fecha_visita, a.tipo_visita, 
                    a.grupo_id, a.estado
                FROM aplicaciones a
                JOIN sitios s ON a.sitio_id = s.id
                WHERE a.participante_id = (
                    SELECT cedula_identidad FROM usuarios WHERE nombre_usuario = %s
                )
            """
            cursor.execute(query, (nombre_usuario,))
            applications = cursor.fetchall()
            
            user_applications = []
            for app in applications:
                user_applications.append({
                    "id": app[0],
                    "sitio_id": app[1],
                    "nombre_sitio": app[2],
                    "participante_id": app[3],
                    "contacto_emergencia": app[4],
                    "fecha_visita": app[5],
                    "tipo_visita": app[6],
                    "grupo_id": app[7],
                    "estado": app[8] if app[8] is not None else "pendiente"
                })
                
            return user_applications