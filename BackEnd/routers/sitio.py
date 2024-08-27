from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from models.sitio import Sitio as SiteModel
from schemas.sitio import SitioCreate, Sitio as SiteSchema
from database import get_db

router = APIRouter()

@router.post("/sitios", response_model=SiteSchema)
def create_site(site: SitioCreate, db: Session = Depends(get_db)):
    db_site = SiteModel(
        titulo=site.titulo,
        descripcion=site.descripcion,
        requisitos=site.requisitos,
        vestimenta=site.vestimenta,
        restricciones=site.restricciones,
        disponibilidad=site.disponibilidad,
        activo=site.activo
    )
    db.add(db_site)
    db.commit()
    db.refresh(db_site)
    return db_site

@router.get("/sitio/{id}", response_model=SiteSchema)
def get_site(id: int, db: Session = Depends(get_db)):
    site = db.query(SiteModel).filter(SiteModel.id == id).first()
    if not site:
        raise HTTPException(status_code=404, detail="Sitio no encontrado")
    return site

@router.get("/sitios", response_model=List[SiteSchema])
def get_sites(db: Session = Depends(get_db)):
    sites = db.query(SiteModel).all()
    return sites
