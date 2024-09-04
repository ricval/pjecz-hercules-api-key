"""
Web Ramas v4, CRUD (create, read, update, and delete)
"""

from typing import Any

from sqlalchemy.orm import Session

from lib.exceptions import MyIsDeletedError, MyNotExistsError, MyNotValidParamError
from lib.safe_string import safe_clave

from hercules.core.web_ramas.models import WebRama


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
