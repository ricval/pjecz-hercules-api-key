"""
Exh Exhortos, esquemas de pydantic
"""

from datetime import date, datetime

from pydantic import BaseModel, ConfigDict


class ExhExhortoOut(BaseModel):
    """Esquema para entregar exhortos"""

    id: int
    autoridad_clave: str
    # municipio_origen_nombre: str
    exhorto_origen_id: str
    remitente: str
    estado: str
    model_config = ConfigDict(from_attributes=True)


class OneExhExhortoOut(BaseModel):
    """Esquema para entrega un exhorto"""

    success: bool
    message: str
    data: ExhExhortoOut | None = None
