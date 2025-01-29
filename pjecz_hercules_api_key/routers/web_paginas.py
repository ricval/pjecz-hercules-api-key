"""
Web Paginas v4, rutas (paths)
"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound

from ..dependencies.authentications import UsuarioInDB, get_current_active_user
from ..dependencies.database import Session, get_db
from ..dependencies.fastapi_pagination_custom_page import CustomPage
from ..dependencies.safe_string import safe_clave
from ..models.permisos import Permiso
from ..models.web_paginas import WebPagina
from ..models.web_ramas import WebRama
from ..schemas.web_paginas import OneWebPaginaOut, WebPaginaOut

web_paginas = APIRouter(prefix="/v4/web_paginas", tags=["sitio web"])


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
        clave = safe_clave(clave)
    except ValueError:
        return OneWebPaginaOut(success=False, message="La clave no es válida")
    try:
        web_pagina = database.query(WebPagina).filter_by(clave=clave).one()
    except (MultipleResultsFound, NoResultFound):
        return OneWebPaginaOut(success=False, message="No existe esa página")
    if web_pagina.estatus != "A":
        return OneWebPaginaOut(success=False, message="No es activa esa página, está eliminada")
    return OneWebPaginaOut.model_validate(web_pagina)


@web_paginas.get("", response_model=CustomPage[WebPaginaOut])
async def paginado_web_paginas(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    clave: str = None,
):
    """Paginado de WebPagina"""
    if current_user.permissions.get("WEB PAGINAS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    consulta = database.query(WebPagina)
    if clave is not None:
        try:
            clave = safe_clave(clave)
        except ValueError:
            return CustomPage(success=False, message="La clave no es válida")
        try:
            web_rama = database.query(WebRama).filter_by(clave=clave).filter_by(estatus="A").one()
            consulta = consulta.filter_by(web_rama_id=web_rama.id)
        except (MultipleResultsFound, NoResultFound):
            return CustomPage(success=False, message="No existe esa rama o está eliminada")
    return paginate(consulta.filter_by(estatus="A").order_by(WebPagina.clave))
