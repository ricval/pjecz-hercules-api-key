"""
Web Paginas v4, rutas (paths)
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
from ..models.web_paginas import WebPagina
from ..schemas.web_paginas import OneWebPaginaOut, WebPaginaOut
from .web_ramas import get_web_rama_with_clave

web_paginas = APIRouter(prefix="/v4/web_paginas", tags=["sitio web"])


def get_web_paginas(
    database: Session,
    web_rama_clave: str = None,
) -> Any:
    """Consultar WebPagina activas"""
    consulta = database.query(WebPagina)
    if web_rama_clave is not None:
        web_rama = get_web_rama_with_clave(database, web_rama_clave)
        consulta = consulta.filter_by(web_rama_id=web_rama.id)
    return consulta.filter_by(estatus="A").order_by(WebPagina.clave)


def get_web_pagina_with_clave(
    database: Session,
    web_pagina_clave: str,
) -> WebPagina:
    """Consultar un WebPagina por su clave"""
    try:
        clave = safe_clave(web_pagina_clave)
    except ValueError as error:
        raise MyNotValidParamError(str(error)) from error
    web_pagina = database.query(WebPagina).filter_by(clave=clave).first()
    if web_pagina is None:
        raise MyNotExistsError("No existe esa página")
    if web_pagina.estatus != "A":
        raise MyIsDeletedError("No es activa esa página, está eliminada")
    return web_pagina


@web_paginas.get("", response_model=CustomPage[WebPaginaOut])
async def paginado_web_paginas(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    web_rama_clave: str = None,
):
    """Paginado de WebPagina"""
    if current_user.permissions.get("WEB PAGINAS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        resultados = get_web_paginas(database, web_rama_clave)
    except MyAnyError as error:
        return CustomPage(success=False, message=str(error))
    return paginate(resultados)


@web_paginas.get("/{clave}", response_model=OneWebPaginaOut)
async def detalle_web_pagina(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    clave: str,
):
    """Detalle de una WebPagina a partir de su clave"""
    if current_user.permissions.get("WEB PAGINAS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        web_pagina = get_web_pagina_with_clave(database, clave)
    except MyAnyError as error:
        return OneWebPaginaOut(success=False, message=str(error))
    return OneWebPaginaOut.model_validate(web_pagina)
