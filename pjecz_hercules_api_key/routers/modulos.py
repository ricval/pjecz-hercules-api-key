"""
Modulos v4, rutas (paths)
"""

from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate

from ..dependencies.authentications import UsuarioInDB, get_current_active_user
from ..dependencies.database import Session, get_db
from ..dependencies.exceptions import MyAnyError, MyIsDeletedError, MyNotExistsError, MyNotValidParamError
from ..dependencies.fastapi_pagination_custom_page import CustomPage
from ..dependencies.safe_string import safe_string
from ..models.modulos import Modulo
from ..models.permisos import Permiso
from ..schemas.modulos import ModuloOut, OneModuloOut

modulos = APIRouter(prefix="/v4/modulos", tags=["usuarios"])


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


@modulos.get("", response_model=CustomPage[ModuloOut])
async def paginado_modulos(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
):
    """Paginado de modulos"""
    if current_user.permissions.get("MODULOS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        resultados = get_modulos(database)
    except MyAnyError as error:
        return CustomPage(success=False, message=str(error))
    return paginate(resultados)


@modulos.get("/{modulo_id}", response_model=OneModuloOut)
async def detalle_modulo(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    modulo_id: int,
):
    """Detalle de un modulo a partir de su id"""
    if current_user.permissions.get("MODULOS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        modulo = get_modulo(database, modulo_id)
    except MyAnyError as error:
        return OneModuloOut(success=False, message=str(error))
    return OneModuloOut.model_validate(modulo)
