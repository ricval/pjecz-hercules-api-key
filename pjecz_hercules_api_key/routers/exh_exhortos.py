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
from ..models.exh_exhortos import ExhExhorto
from ..models.permisos import Permiso
from ..schemas.exh_exhortos import ExhExhortoOut, OneExhExhortoOut

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
            # raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No es válida la clave de la autoridad")
        consulta = consulta.join(Autoridad).filter(Autoridad.clave == autoridad_clave)
    return paginate(consulta.filter(ExhExhorto.estatus == "A").order_by(ExhExhorto.id.desc()))
