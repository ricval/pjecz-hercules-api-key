"""
Autoridades, esquemas de pydantic
"""

from pydantic import BaseModel, ConfigDict

from ..dependencies.schemas_base import OneBaseOut


class AutoridadOut(BaseModel):
    """Esquema para entregar autoridades"""

    id: int
    clave: str
    distrito_clave: str
    distrito_nombre: str
    distrito_nombre_corto: str
    materia_clave: str
    materia_nombre: str
    model_config = ConfigDict(from_attributes=True)


class OneAutoridadOut(OneBaseOut):
    """Esquema para entregar una autoridad"""

    data: AutoridadOut | None = None
