"""
Modulos v4, CRUD (create, read, update, and delete)
"""

from typing import Any

from sqlalchemy.orm import Session

from lib.exceptions import MyIsDeletedError, MyNotExistsError, MyNotValidParamError
from lib.safe_string import safe_string
from hercules.core.modulos.models import Modulo


def get_modulos(database: Session) -> Any:
    """Consultar los modulos activos"""
    return database.query(Modulo).filter_by(estatus="A").order_by(Modulo.nombre)


def get_modulo(database: Session, modulo_id: int) -> Modulo:
    """Consultar un modulo por su id"""
    modulo = database.query(Modulo).get(modulo_id)
    if modulo is None:
        raise MyNotExistsError("No existe ese modulo")
    if modulo.estatus != "A":
        raise MyIsDeletedError("No es activo ese modulo, está eliminado")
    return modulo


def get_modulo_with_nombre(database: Session, modulo_nombre: str) -> Modulo:
    """Consultar un modulo por su nombre"""
    try:
        nombre = safe_string(modulo_nombre)
    except ValueError as error:
        raise MyNotValidParamError(str(error)) from error
    modulo = database.query(Modulo).filter_by(nombre=nombre).first()
    if modulo is None:
        raise MyNotExistsError("No existe ese modulo")
    if modulo.estatus != "A":
        raise MyIsDeletedError("No es activo ese modulo, está eliminado")
    return modulo
