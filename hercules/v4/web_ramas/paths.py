"""
Web Ramas v4, rutas (paths)
"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate

from lib.database import Session, get_db
from lib.exceptions import MyAnyError
from lib.fastapi_pagination_custom_page import CustomPage

from hercules.core.permisos.models import Permiso
from hercules.v4.web_ramas.crud import get_web_rama_with_clave, get_web_ramas
from hercules.v4.web_ramas.schemas import OneWebRamaOut, WebRamaOut
from hercules.v4.usuarios.authentications import UsuarioInDB, get_current_active_user

web_ramas = APIRouter(prefix="/v4/web_ramas", tags=["sitio web"])


@web_ramas.get("", response_model=CustomPage[WebRamaOut])
async def paginado_web_ramas(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
):
    """Paginado de web_ramas"""
    if current_user.permissions.get("WEB RAMAS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        resultados = get_web_ramas(database)
    except MyAnyError as error:
        return CustomPage(success=False, message=str(error))
    return paginate(resultados)


@web_ramas.get("/{clave}", response_model=OneWebRamaOut)
async def detalle_web_rama(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    clave: str,
):
    """Detalle de una web_ramas a partir de su clave"""
    if current_user.permissions.get("WEB RAMAS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        web_rama = get_web_rama_with_clave(database, clave)
    except MyAnyError as error:
        return OneWebRamaOut(success=False, message=str(error))
    return OneWebRamaOut.model_validate(web_rama)
