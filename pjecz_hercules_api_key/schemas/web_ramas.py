"""
Web Ramas v4, esquemas de pydantic
"""

from pydantic import BaseModel, ConfigDict

from ..dependencies.schemas_base import OneBaseOut


class WebRamaOut(BaseModel):
    """Esquema para entregar WebRama"""

    clave: str | None = None
    nombre: str | None = None
    model_config = ConfigDict(from_attributes=True)


class OneWebRamaOut(WebRamaOut, OneBaseOut):
    """Esquema para entregar una WebRama"""
