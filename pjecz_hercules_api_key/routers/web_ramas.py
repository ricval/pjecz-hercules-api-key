"""
Web Ramas v4, rutas (paths)
"""

from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate

from ..dependencies.authentications import UsuarioInDB, get_current_active_user
from ..dependencies.database import Session, get_db
from ..dependencies.exceptions import MyAnyError, MyIsDeletedError, MyNotExistsError, MyNotValidParamError
from ..dependencies.fastapi_pagination_custom_page import CustomPage
from ..dependencies.safe_string import safe_clave
from ..models.permisos import Permiso
from ..models.web_ramas import WebRama
from ..schemas.web_ramas import OneWebRamaOut, WebRamaOut

web_ramas = APIRouter(prefix="/v4/web_ramas", tags=["sitio web"])


def get_web_ramas(database: Session) -> Any:
    """Consultar WebRama activas"""
    return database.query(WebRama).filter_by(estatus="A").order_by(WebRama.nombre)


def get_web_rama_with_clave(database: Session, web_rama_clave: str) -> WebRama:
    """Consultar un WebRama por su clave"""
    try:
        clave = safe_clave(web_rama_clave)
    except ValueError as error:
        raise MyNotValidParamError(str(error)) from error
    web_rama = database.query(WebRama).filter_by(clave=clave).first()
    if web_rama is None:
        raise MyNotExistsError("No existe esa rama")
    if web_rama.estatus != "A":
        raise MyIsDeletedError("No es activo esa rama, está eliminada")
    return web_rama


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
