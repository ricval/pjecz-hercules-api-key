"""
PJECZ Hércules API Key
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination

from .routers.modulos import modulos
from .routers.permisos import permisos
from .routers.roles import roles
from .routers.usuarios import usuarios
from .routers.usuarios_roles import usuarios_roles
from .routers.web_paginas import web_paginas
from .routers.web_ramas import web_ramas
from .settings import get_settings

# FastAPI
app = FastAPI(
    title="API pública del Poder Judicial del Estado de Coahuila de Zaragoza",
    description="Para consultar la base de datos Plataforma Web. Para solicitar api-key escriba a informatica en pjecz.gob.mx.",
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
app.include_router(modulos)
app.include_router(permisos)
app.include_router(roles)
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
