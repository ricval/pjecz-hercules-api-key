"""
Web Paginas v4, rutas (paths)
"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate

from lib.database import Session, get_db
from lib.exceptions import MyAnyError
from lib.fastapi_pagination_custom_page import CustomPage

from hercules.core.permisos.models import Permiso
from hercules.v4.web_paginas.crud import get_web_pagina_with_clave, get_web_paginas
from hercules.v4.web_paginas.schemas import OneWebPaginaOut, WebPaginaOut
from hercules.v4.usuarios.authentications import UsuarioInDB, get_current_active_user

web_paginas = APIRouter(prefix="/v4/web_paginas", tags=["sitio web"])


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
