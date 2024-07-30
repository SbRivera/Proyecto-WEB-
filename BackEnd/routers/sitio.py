from fastapi import APIRouter, HTTPException
from models.sitio import Site
from .database import get_db
from psycopg2 import sql

router = APIRouter()

@router.post("/sitios")
def create_site(site: Site):
    with get_db() as conn:
        with conn.cursor() as cursor:
            query = sql.SQL("""
                INSERT INTO sitios (titulo, descripcion, requisitos, vestimenta, restricciones, disponibilidad, activo)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """)
            cursor.execute(query, (
                site.titulo,
                site.descripcion,
                site.requisitos,
                site.vestimenta,
                site.restricciones,
                site.disponibilidad,
                site.activo
            ))
            conn.commit()
    return {"message": "Sitio creado exitosamente"}

@router.get("/sitio/{id}")
def get_site(id: int):
    with get_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT titulo, descripcion, requisitos, vestimenta, restricciones, disponibilidad, activo
                FROM sitios WHERE id = %s
            """, (id,))
            site_data = cursor.fetchone()
            if site_data:
                return {
                    "titulo": site_data[0],
                    "descripcion": site_data[1],
                    "requisitos": site_data[2],
                    "vestimenta": site_data[3],
                    "restricciones": site_data[4],
                    "disponibilidad": site_data[5],
                    "activo": site_data[6]
                }
            raise HTTPException(status_code=404, detail="Sitio no encontrado")

@router.get("/sitios")
def get_sites():
    with get_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT id, titulo, descripcion, requisitos, vestimenta, restricciones, disponibilidad, activo
                FROM sitios
            """)
            sites_data = cursor.fetchall()
            return [
                {
                    "id": site[0],
                    "titulo": site[1],
                    "descripcion": site[2],
                    "requisitos": site[3],
                    "vestimenta": site[4],
                    "restricciones": site[5],
                    "disponibilidad": site[6],
                    "activo": site[7]
                }
                for site in sites_data
            ]
