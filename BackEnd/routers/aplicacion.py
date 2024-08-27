from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from models.aplicacion import Aplicacion
from models.sitio import Sitio
from models.usuario import Usuario
from schemas.aplicacion import AplicacionCreate, AplicacionUpdate
from database import get_db
import uuid
from datetime import datetime

router = APIRouter()

@router.post("/aplicaciones", response_model=Dict[str, Any])
def create_aplicacion(aplicacion: AplicacionCreate, db: Session = Depends(get_db)):
    grupo_id = uuid.UUID(str(uuid.uuid4()))
    for participant_id in aplicacion.participant_ids:
        db_aplicacion = Aplicacion(
            sitio_id=aplicacion.sitio_id,
            participante_id=participant_id,
            contacto_emergencia=aplicacion.contacto_emergencia,
            fecha_visita=aplicacion.fecha_visita,
            tipo_visita=aplicacion.tipo_visita,
            grupo_id=grupo_id,
            estado=None
        )
        db.add(db_aplicacion)
    db.commit()
    return {"message": "Solicitud enviada exitosamente", "grupo_id": grupo_id}

@router.get("/aplicaciones", response_model=List[Dict[str, Any]])
def read_aplicaciones(db: Session = Depends(get_db)):
    aplicaciones = db.query(
        Aplicacion.id,
        Aplicacion.sitio_id,
        Sitio.titulo.label('nombre_sitio'),
        Aplicacion.participante_id,
        Usuario.nombre_completo.label('nombre_participante'),
        Aplicacion.contacto_emergencia,
        Aplicacion.fecha_visita,
        Aplicacion.tipo_visita,
        Aplicacion.grupo_id,
        Aplicacion.estado
    ).join(Sitio).join(Usuario, Aplicacion.participante_id == Usuario.cedula_identidad).filter(Aplicacion.fecha_visita >= datetime.now()).all()

    grouped_applications = {}
    for app in aplicaciones:
        grupo_id = app.grupo_id
        if grupo_id not in grouped_applications:
            grouped_applications[grupo_id] = {
                "id": app.id,
                "sitio_id": app.sitio_id,
                "nombre_sitio": app.nombre_sitio,
                "contacto_emergencia": app.contacto_emergencia,
                "fecha_visita": app.fecha_visita,
                "tipo_visita": app.tipo_visita,
                "grupo_id": app.grupo_id,
                "estado": app.estado,
                "participants": []
            }
        grouped_applications[grupo_id]["participants"].append({
            "cedula": app.participante_id,
            "nombre": app.nombre_participante
        })

    return list(grouped_applications.values())

@router.put("/aplicaciones/estado")
def update_application_status(update: AplicacionUpdate, db: Session = Depends(get_db)):
    aplicaciones = db.query(Aplicacion).filter(Aplicacion.grupo_id == update.grupo_id).all()
    if not aplicaciones:
        raise HTTPException(status_code=404, detail="Solicitud no encontrada")
    for aplicacion in aplicaciones:
        aplicacion.estado = update.estado
    db.commit()
    return {"message": "Estado de la solicitud actualizado exitosamente"}

@router.get("/aplicaciones/{nombre_usuario}", response_model=List[Dict[str, Any]])
def get_user_applications(nombre_usuario: str, db: Session = Depends(get_db)):
    user_cedula = db.query(Usuario.cedula_identidad).filter(Usuario.nombre_usuario == nombre_usuario).scalar()
    if not user_cedula:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    aplicaciones_usuario  = db.query(
        Aplicacion.id,
        Aplicacion.sitio_id,
        Sitio.titulo.label('nombre_sitio'),
        Usuario.cedula_identidad.label('cedula'),
        Usuario.nombre_completo.label('nombre'),
        Aplicacion.contacto_emergencia,
        Aplicacion.fecha_visita,
        Aplicacion.tipo_visita,
        Aplicacion.grupo_id,
        Aplicacion.estado
    ).join(Sitio).join(Usuario).filter(Aplicacion.participante_id == user_cedula).all()

    grupo_ids = [app.grupo_id for app in aplicaciones_usuario]

    if grupo_ids:
        aplicaciones_grupo = db.query(
            Aplicacion.id,
            Aplicacion.sitio_id,
            Sitio.titulo.label('nombre_sitio'),
            Usuario.cedula_identidad.label('cedula'),
            Usuario.nombre_completo.label('nombre'),
            Aplicacion.contacto_emergencia,
            Aplicacion.fecha_visita,
            Aplicacion.tipo_visita,
            Aplicacion.grupo_id,
            Aplicacion.estado
        ).join(Sitio).join(Usuario).filter(Aplicacion.grupo_id.in_(grupo_ids)).all()
    else:
        aplicaciones_grupo = []

    todas_aplicaciones = aplicaciones_usuario + aplicaciones_grupo

    grouped_applications = {}
    for app in todas_aplicaciones:
        grupo_id = app.grupo_id
        if grupo_id not in grouped_applications:
            grouped_applications[grupo_id] = {
                "id": app.id,
                "sitio_id": app.sitio_id,
                "nombre_sitio": app.nombre_sitio,
                "contacto_emergencia": app.contacto_emergencia,
                "fecha_visita": app.fecha_visita,
                "tipo_visita": app.tipo_visita,
                "grupo_id": app.grupo_id,
                "estado": app.estado,
                "participants": []
            }
        grouped_applications[grupo_id]["participants"].append({
            "cedula": app.cedula,
            "nombre": app.nombre
        })

    return list(grouped_applications.values())