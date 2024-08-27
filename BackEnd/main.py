from routers import usuario, sitio, aplicacion
from database import engine, Base
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


Base.metadata.create_all(bind=engine)

app.include_router(usuario.router)
app.include_router(sitio.router)
app.include_router(aplicacion.router)
