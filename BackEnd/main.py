from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import usuario, sitio, aplicacion

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(usuario.router)
app.include_router(sitio.router)
app.include_router(aplicacion.router)

