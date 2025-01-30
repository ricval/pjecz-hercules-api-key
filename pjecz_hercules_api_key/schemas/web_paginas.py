"""
Web Paginas v4, esquemas de pydantic
"""

from datetime import date

from pydantic import BaseModel, ConfigDict

from ..dependencies.schemas_base import OneBaseOut


class WebPaginaOut(BaseModel):
    """Esquema para items de WebPagina"""

    clave: str | None = None
    contenido: str | None = None
    etiquetas: str | None = None
    estado: str | None = None
    fecha_modificacion: date | None = None
    responsable: str | None = None
    resumen: str | None = None
    ruta: str | None = None
    titulo: str | None = None
    vista_previa: str | None = None
    model_config = ConfigDict(from_attributes=True)


class OneWebPaginaOut(OneBaseOut):
    """Esquema para entregar una WebPagina"""

    data: WebPaginaOut | None = None
