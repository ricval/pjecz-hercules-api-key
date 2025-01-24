"""
Roles v4, rutas (paths)
"""

from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate

from ..dependencies.authentications import UsuarioInDB, get_current_active_user
from ..dependencies.database import Session, get_db
from ..dependencies.exceptions import MyAnyError, MyIsDeletedError, MyNotExistsError, MyNotValidParamError
from ..dependencies.fastapi_pagination_custom_page import CustomPage
from ..dependencies.safe_string import safe_string
from ..models.permisos import Permiso
from ..models.roles import Rol
from ..schemas.roles import OneRolOut, RolOut

roles = APIRouter(prefix="/v4/roles", tags=["usuarios"])


def get_roles(database: Session) -> Any:
    """Consultar los roles activos"""
    return database.query(Rol).filter_by(estatus="A").order_by(Rol.nombre)


def get_rol(database: Session, rol_id: int) -> Rol:
    """Consultar un rol por su id"""
    rol = database.query(Rol).get(rol_id)
    if rol is None:
        raise MyNotExistsError("No existe ese rol")
    if rol.estatus != "A":
        raise MyIsDeletedError("No es activo ese rol, está eliminado")
    return rol


def get_rol_with_nombre(database: Session, rol_nombre: str) -> Rol:
    """Consultar un rol por su nombre"""
    try:
        nombre = safe_string(rol_nombre)
    except ValueError as error:
        raise MyNotValidParamError(str(error)) from error
    rol = database.query(Rol).filter_by(nombre=nombre).first()
    if rol is None:
        raise MyNotExistsError("No existe ese rol")
    if rol.estatus != "A":
        raise MyIsDeletedError("No es activo ese rol, está eliminado")
    return rol


@roles.get("", response_model=CustomPage[RolOut])
async def paginado_roles(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
):
    """Paginado de roles"""
    if current_user.permissions.get("ROLES", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        resultados = get_roles(database)
    except MyAnyError as error:
        return CustomPage(success=False, message=str(error))
    return paginate(resultados)


@roles.get("/{rol_id}", response_model=OneRolOut)
async def detalle_rol(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    rol_id: int,
):
    """Detalle de una rol a partir de su nombre"""
    if current_user.permissions.get("ROLES", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        rol = get_rol(database, rol_id)
    except MyAnyError as error:
        return OneRolOut(success=False, message=str(error))
    return OneRolOut.model_validate(rol)
