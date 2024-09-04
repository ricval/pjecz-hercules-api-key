"""
Web Paginas v4, CRUD (create, read, update, and delete)
"""

from typing import Any

from sqlalchemy.orm import Session

from lib.exceptions import MyIsDeletedError, MyNotExistsError, MyNotValidParamError
from lib.safe_string import safe_clave

from hercules.core.web_paginas.models import WebPagina
from hercules.v4.web_ramas.crud import get_web_rama_with_clave


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
