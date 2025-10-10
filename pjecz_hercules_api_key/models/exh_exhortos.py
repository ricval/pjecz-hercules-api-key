"""
Exh Exhortos, modelos
"""

from datetime import date, datetime
from typing import Optional

from sqlalchemy import JSON, Enum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..dependencies.database import Base
from ..dependencies.universal_mixin import UniversalMixin


class ExhExhorto(Base, UniversalMixin):
    """ExhExhorto"""

    ESTADOS = {
        "RECIBIDO": "Recibido",
        "TRANSFIRIENDO": "Transfiriendo",
        "PROCESANDO": "Procesando",
        "RECHAZADO": "Rechazado",
        "CONTESTADO": "Contestado",
        "PENDIENTE": "Pendiente",
        "CANCELADO": "Cancelado",
        "POR ENVIAR": "Por enviar",
        "RECIBIDO CON EXITO": "Recibido con éxito",
        "RESPONDIDO": "Respondido",
        "ARCHIVADO": "Archivado",
    }

    REMITENTES = {
        "INTERNO": "Interno",
        "EXTERNO": "Externo",
    }

    # Nombre de la tabla
    __tablename__ = "exh_exhortos"

    # Clave primaria
    id: Mapped[int] = mapped_column(primary_key=True)

    # Clave foránea: Autoridad, Juzgado/Área al que se turna el Exhorto y hará el correspondiente proceso de este
    autoridad_id: Mapped[int] = mapped_column(ForeignKey("autoridades.id"))
    autoridad: Mapped["Autoridad"] = relationship(back_populates="exh_exhortos")

    # Clave foránea: Área de recepción
    # exh_area_id: Mapped[int] = mapped_column(ForeignKey("exh_areas.id"))
    # exh_area: Mapped["ExhArea"] = relationship(back_populates="exh_exhortos")

    # Clave foránea: Tipo de diligencia
    # exh_tipo_diligencia_id: Mapped[int] = mapped_column(ForeignKey("exh_tipos_diligencias.id"))
    # exh_tipo_diligencia: Mapped["ExhTipoDiligencia"] = relationship(back_populates="exh_exhortos")

    # Clave foránea: Municipio de Origen donde está localizado el Juzgado del PJ exhortante
    # Cuando haya comunicación por medio de la API se debe recibir o transmitir el identificador INEGI del municipio
    # municipio_origen_id: Mapped[int] = mapped_column(ForeignKey("municipios.id"))
    # municipio_origen: Mapped["Municipio"] = relationship(back_populates="exh_exhortos_origenes")

    # UUID identificador con el que el PJ exhortante identifica el exhorto que envía
    exhorto_origen_id: Mapped[str] = mapped_column(String(64))

    # Campo para saber si es un proceso interno o extorno
    remitente: Mapped[str] = mapped_column(Enum(*REMITENTES, name="exh_exhortos_remitentes", native_enum=False), index=True)

    # Estado del exhorto y el estado anterior, para cuando
    estado: Mapped[str] = mapped_column(Enum(*ESTADOS, name="exh_exhortos_estados", native_enum=False), index=True)

    @property
    def autoridad_clave(self):
        """Regresa la clave de la autoridad"""
        return self.autoridad.clave

    # @property
    # def municipio_origen_nombre(self):
    #     """Regresa el nombre del municipio de origen"""
    #     return self.municipio_origen.nombre

    def __repr__(self):
        """Representación"""
        return f"<ExhExhorto {self.id}>"
