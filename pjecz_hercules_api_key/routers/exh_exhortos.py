"""
Listas de Acuerdos
"""

from datetime import date
from io import BytesIO
from typing import Annotated
from urllib.parse import unquote, urlparse

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from fastapi_pagination.ext.sqlalchemy import paginate
from google.cloud import storage
from hashids import Hashids

from ..config.settings import Settings, get_settings
from ..dependencies.authentications import UsuarioInDB, get_current_active_user
from ..dependencies.database import Session, get_db
from ..dependencies.fastapi_pagination_custom_page import CustomPage
from ..dependencies.safe_string import safe_clave
from ..models.autoridades import Autoridad
from ..models.exh_areas import ExhArea
from ..models.exh_exhortos import ExhExhorto
from ..models.exh_tipos_diligencias import ExhTipoDiligencia
from ..models.materias import Materia
from ..models.municipios import Municipio
from ..models.permisos import Permiso
from ..schemas.exh_exhortos import ExhExhortoIn, ExhExhortoOut, OneExhExhortoOut

exh_exhortos = APIRouter(prefix="/api/v5/exh_exhortos", tags=["exhortos"])


@exh_exhortos.get("/{exh_exhorto_id}", response_model=OneExhExhortoOut)
async def detalle(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    exh_exhorto_id: int,
):
    """Detalle de un exhorto a partir de su ID"""
    if current_user.permissions.get("EXH EXHORTOS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    exh_exhorto = database.query(ExhExhorto).get(exh_exhorto_id)
    if exh_exhorto is None:
        return OneExhExhortoOut(success=False, message="No existe ese exhorto")
    if exh_exhorto.estatus != "A":
        return OneExhExhortoOut(success=False, message="No es activo ese exhorto, está eliminado")
    return OneExhExhortoOut(
        success=True,
        message="Detalle del exhorto",
        data=ExhExhortoOut.model_validate(exh_exhorto),
    )


@exh_exhortos.get("", response_model=CustomPage[ExhExhortoOut])
async def paginado(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    autoridad_clave: str = "",
):
    """Paginado de exh_exhortos"""
    if current_user.permissions.get("EXH EXHORTOS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    consulta = database.query(ExhExhorto)
    if autoridad_clave:
        try:
            autoridad_clave = safe_clave(autoridad_clave)
        except ValueError:
            return CustomPage(success=False, message="No es válida la clave de la autoridad")
        consulta = consulta.join(Autoridad).filter(Autoridad.clave == autoridad_clave)
    return paginate(consulta.filter(ExhExhorto.estatus == "A").order_by(ExhExhorto.id.desc()))


@exh_exhortos.post("", response_model=OneExhExhortoOut)
async def crear(
    exh_exhorto_in: ExhExhortoIn,
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    settings: Annotated[Settings, Depends(get_settings)],
):
    """Crear un exhorto"""
    if current_user.permissions.get("EXH EXHORTOS", 0) < Permiso.CREAR:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

    # Validar la autoridad
    try:
        exh_exhorto_in.autoridad_clave = safe_clave(exh_exhorto_in.autoridad_clave)
    except ValueError:
        return OneExhExhortoOut(success=False, message="No es válida la clave de la autoridad")
    autoridad = database.query(Autoridad).filter(Autoridad.clave == exh_exhorto_in.autoridad_clave).first()
    if autoridad is None:
        return OneExhExhortoOut(success=False, message="No existe esa autoridad")
    if autoridad.estatus != "A":
        return OneExhExhortoOut(success=False, message="Esa autoridad no está activa")

    # Validar el área
    try:
        exh_exhorto_in.exh_area_clave = safe_clave(exh_exhorto_in.exh_area_clave)
    except ValueError:
        return OneExhExhortoOut(success=False, message="No es válida la clave del área")
    exh_area = database.query(ExhArea).filter(ExhArea.clave == exh_exhorto_in.exh_area_clave).first()
    if exh_area is None:
        return OneExhExhortoOut(success=False, message="No existe ese área")
    if exh_area.estatus != "A":
        return OneExhExhortoOut(success=False, message="Ese área no está activa")

    # Validar el municipio de origen
    municipio_origen = database.query(Municipio).get(exh_exhorto_in.municipio_origen_id)
    if municipio_origen is None:
        return OneExhExhortoOut(success=False, message="No existe ese municipio de origen")
    if municipio_origen.estatus != "A":
        return OneExhExhortoOut(success=False, message="Ese municipio está inactivo")

    # Validar el municipio de destino
    municipio_destino = database.query(Municipio).get(exh_exhorto_in.municipio_destino_id)
    if municipio_destino is None:
        return OneExhExhortoOut(success=False, message="No existe ese municipio de destino")
    if municipio_destino.estatus != "A":
        return OneExhExhortoOut(success=False, message="Ese municipio está inactivo")

    # Validar la materia
    try:
        exh_exhorto_in.materia_clave = safe_clave(exh_exhorto_in.materia_clave)
    except ValueError:
        return OneExhExhortoOut(success=False, message="No es válida la clave de la materia")
    materia = database.query(Materia).filter(Materia.clave == exh_exhorto_in.materia_clave).first()
    if materia is None:
        return OneExhExhortoOut(success=False, message="No existe esa materia")
    if materia.estatus != "A":
        return OneExhExhortoOut(success=False, message="Esa materia no está activa")

    # Consultar el tipo de diligencia con clave "OTR" (OTROS)
    exh_tipo_diligencia = database.query(ExhTipoDiligencia).filter(ExhTipoDiligencia.clave == "OTR").first()
    if exh_tipo_diligencia is None:
        return OneExhExhortoOut(success=False, message='No existe el tipo de diligencia con clave "OTR"')
    if exh_tipo_diligencia.estatus != "A":
        return OneExhExhortoOut(success=False, message='El tipo de diligencia con clave "OTR" no está activo')

    # Crear el exhorto
    exh_exhorto = ExhExhorto(
        autoridad_id=autoridad.id,
        exh_area_id=exh_area.id,
        exh_tipo_diligencia_id=exh_tipo_diligencia.id,
        municipio_origen_id=municipio_origen.id,
        exhorto_origen_id=exh_exhorto_in.exhorto_origen_id,
        municipio_destino_id=municipio_destino.id,
        materia_clave=materia.clave,
        materia_nombre=materia.nombre,
        tipo_juicio_asunto_delitos=exh_exhorto_in.tipo_juicio_asunto_delitos,
        fojas=exh_exhorto_in.fojas,
        dias_responder=exh_exhorto_in.dias_responder,
        remitente="INTERNO",
        estado="PENDIENTE",
    )
    database.add(exh_exhorto)
    database.commit()
    database.refresh(exh_exhorto)

    # Entregar
    return OneExhExhortoOut(
        success=True,
        message="Exhorto creado",
        data=ExhExhortoOut.model_validate(exh_exhorto),
    )
