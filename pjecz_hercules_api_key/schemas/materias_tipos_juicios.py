"""
Materias Tipos de Juicios, esquemas de pydantic
"""

from pydantic import BaseModel, ConfigDict

from ..dependencies.schemas_base import OneBaseOut


class MateriaTipoJuicioOut(BaseModel):
    """Esquema para entregar materias-tipos de juicios"""

    id: int
    materia_clave: str
    materia_nombre: str
    descripcion: str
    model_config = ConfigDict(from_attributes=True)


class OneMateriaTipoJuicioOut(OneBaseOut):
    """Esquema para entregar una materia-tipo de juicio"""

    data: MateriaTipoJuicioOut | None = None
