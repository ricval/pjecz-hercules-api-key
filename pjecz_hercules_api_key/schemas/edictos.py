"""
Edictos, esquemas de pydantic
"""

from datetime import date, datetime

from pydantic import BaseModel, ConfigDict

from ..dependencies.schemas_base import OneBaseOut


class EdictoOut(BaseModel):
    """Esquema para entregar edictos"""

    id: int
    distrito_clave: str
    distrito_nombre: str
    distrito_nombre_corto: str
    autoridad_clave: str
    autoridad_descripcion: str
    autoridad_descripcion_corta: str
    fecha: date
    descripcion: str
    expediente: str
    numero_publicacion: str
    es_declaracion_de_ausencia: bool = False
    model_config = ConfigDict(from_attributes=True)


class EdictoRAGOut(EdictoOut):
    """Agregar los campos RAG para cuando se entrega un edicto"""

    rag_fue_analizado_tiempo: datetime | None = None
    rag_analisis: dict | None = None
    rag_fue_sintetizado_tiempo: datetime | None = None
    rag_sintesis: dict | None = None
    rag_fue_categorizado_tiempo: datetime | None = None
    rag_categorias: dict | None = None


class OneEdictoOut(OneBaseOut):
    """Esquema para entregar un edicto"""

    data: EdictoRAGOut | None = None
