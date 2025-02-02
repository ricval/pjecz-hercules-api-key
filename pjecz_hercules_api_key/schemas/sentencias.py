"""
Sentencias, esquemas de pydantic
"""

from datetime import date, datetime

from pydantic import BaseModel, ConfigDict

from ..dependencies.schemas_base import OneBaseOut


class SentenciaOut(BaseModel):
    """Esquema para entregar sentencias"""

    id: int
    distrito_clave: str
    distrito_nombre: str
    distrito_nombre_corto: str
    autoridad_clave: str
    autoridad_descripcion: str
    autoridad_descripcion_corta: str
    sentencia: str
    sentencia_fecha: date | None = None
    expediente: str
    expediente_anio: int
    expediente_num: int
    fecha: date
    descripcion: str
    es_perspectiva_genero: bool
    model_config = ConfigDict(from_attributes=True)


class SentenciaRAGOut(SentenciaOut):
    """Agregar los campos RAG para cuando se entrega una sentencia"""

    rag_fue_analizado_tiempo: datetime | None = None
    rag_analisis: dict | None = None
    rag_fue_sintetizado_tiempo: datetime | None = None
    rag_sintesis: dict | None = None
    rag_fue_categorizado_tiempo: datetime | None = None
    rag_categorias: dict | None = None


class OneSentenciaOut(OneBaseOut):
    """Esquema para entregar una sentencia"""

    data: SentenciaRAGOut | None = None
