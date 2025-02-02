"""
Web Paginas, esquemas de pydantic
"""

from datetime import date

from pydantic import BaseModel, ConfigDict

from ..dependencies.schemas_base import OneBaseOut


class WebPaginaOut(BaseModel):
    """Esquema para items de WebPagina"""

    id: int
    clave: str
    contenido: str
    etiquetas: str
    estado: str
    fecha_modificacion: date
    responsable: str
    resumen: str
    ruta: str
    titulo: str
    vista_previa: str
    model_config = ConfigDict(from_attributes=True)


class OneWebPaginaOut(OneBaseOut):
    """Esquema para entregar una WebPagina"""

    data: WebPaginaOut | None = None
