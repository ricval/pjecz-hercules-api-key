"""
Edictos
"""

from datetime import date
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate

from ..dependencies.authentications import UsuarioInDB, get_current_active_user
from ..dependencies.database import Session, get_db
from ..dependencies.fastapi_pagination_custom_page import CustomPage
from ..dependencies.safe_string import safe_clave
from ..models.autoridades import Autoridad
from ..models.edictos import Edicto
from ..models.permisos import Permiso
from ..schemas.edictos import EdictoOut, EdictoRAGOut, OneEdictoOut

edictos = APIRouter(prefix="/api/v5/edictos", tags=["edictos"])


@edictos.get("/{edicto_id}", response_model=OneEdictoOut)
async def detalle(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    edicto_id: int,
):
    """Detalle de un edicto a partir de su ID"""
    if current_user.permissions.get("EDICTOS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    edicto = database.query(Edicto).get(edicto_id)
    if edicto is None:
        return OneEdictoOut(success=False, message="No existe ese edicto")
    if edicto.estatus != "A":
        return OneEdictoOut(success=False, message="No es activa ese edicto, está eliminado")
    return OneEdictoOut(success=True, message="Detalle de un edicto", data=EdictoRAGOut.model_validate(edicto))


@edictos.get("", response_model=CustomPage[EdictoOut])
async def paginado(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    autoridad_clave: str = "",
    fecha: date | None = None,
    fecha_desde: date | None = None,
    fecha_hasta: date | None = None,
):
    """Paginado de edictos"""
    if current_user.permissions.get("EDICTOS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    consulta = database.query(Edicto)
    if autoridad_clave:
        try:
            autoridad_clave = safe_clave(autoridad_clave)
        except ValueError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No es válida la clave")
        consulta = consulta.join(Autoridad).filter(Autoridad.clave == autoridad_clave).filter(Autoridad.estatus == "A")
    if fecha is not None:
        consulta = consulta.filter(Edicto.fecha == fecha)
    else:
        if fecha_desde is not None:
            consulta = consulta.filter(Edicto.fecha >= fecha_desde)
        if fecha_hasta is not None:
            consulta = consulta.filter(Edicto.fecha <= fecha_hasta)
    return paginate(consulta.filter(Edicto.estatus == "A").order_by(Edicto.id.desc()))
