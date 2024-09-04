"""
PJECZ Plataforma Web API Key
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination

from config.settings import get_settings

from hercules.v4.modulos.paths import modulos
from hercules.v4.permisos.paths import permisos
from hercules.v4.roles.paths import roles
from hercules.v4.usuarios.paths import usuarios
from hercules.v4.usuarios_roles.paths import usuarios_roles
from hercules.v4.web_paginas.paths import web_paginas
from hercules.v4.web_ramas.paths import web_ramas


def create_app() -> FastAPI:
    """Crea la aplicación FastAPI"""

    # FastAPI
    app = FastAPI(
        title="PJECZ Hércules API Key",
        description="API con autentificación para construir el sitio web.",
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
        return {"message": "API con autentificación para realizar operaciones con la base de datos de Plataforma Web."}

    # Entregar
    return app
