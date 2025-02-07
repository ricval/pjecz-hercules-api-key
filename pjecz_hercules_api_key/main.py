"""
PJECZ Hércules API Key
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination

from .routers.autoridades import autoridades
from .routers.distritos import distritos
from .routers.edictos import edictos
from .routers.listas_de_acuerdos import listas_de_acuerdos
from .routers.materias import materias
from .routers.materias_tipos_juicios import materias_tipos_juicios
from .routers.modulos import modulos
from .routers.permisos import permisos
from .routers.roles import roles
from .routers.sentencias import sentencias
from .routers.usuarios import usuarios
from .routers.usuarios_roles import usuarios_roles
from .routers.web_paginas import web_paginas
from .routers.web_ramas import web_ramas
from .settings import get_settings

# FastAPI
app = FastAPI(
    title="PJECZ API key de Plataforma Web",
    description="API de uso público para consultar edictos, listas de acuerdos, sentencias, etc.",
    docs_url="/docs",
    redoc_url=None,
)

# CORSMiddleware
settings = get_settings()
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.origins.split(","),
    allow_credentials=False,
    allow_methods=["GET"],
    allow_headers=["*"],
)

# Rutas
app.include_router(autoridades)
app.include_router(distritos)
app.include_router(edictos)
app.include_router(listas_de_acuerdos)
app.include_router(materias)
app.include_router(materias_tipos_juicios)
app.include_router(modulos)
app.include_router(permisos)
app.include_router(roles)
app.include_router(sentencias)
app.include_router(usuarios)
app.include_router(usuarios_roles)
app.include_router(web_paginas)
app.include_router(web_ramas)

# Paginación
add_pagination(app)


# Mensaje de Bienvenida
@app.get("/")
async def root():
    """Mensaje de Bienvenida"""
    return {"message": "API del Poder Judicial del Estado de Coahuila de Zaragoza. Solicitudes a informatica en pjecz.gob.mx."}
