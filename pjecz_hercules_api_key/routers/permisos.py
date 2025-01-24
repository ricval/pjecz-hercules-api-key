"""
Permisos v4, rutas (paths)
"""

from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate

from ..dependencies.authentications import UsuarioInDB, get_current_active_user
from ..dependencies.database import Session, get_db
from ..dependencies.exceptions import MyAnyError, MyIsDeletedError, MyNotExistsError
from ..dependencies.fastapi_pagination_custom_page import CustomPage
from ..models.permisos import Permiso
from ..schemas.permisos import OnePermisoOut, PermisoOut
from .modulos import get_modulo
from .roles import get_rol

permisos = APIRouter(prefix="/v4/permisos", tags=["usuarios"])


def get_permisos(
    database: Session,
    modulo_id: int = None,
    rol_id: int = None,
) -> Any:
    """Consultar los permisos activos"""
    consulta = database.query(Permiso)
    if modulo_id is not None:
        modulo = get_modulo(database, modulo_id)
        consulta = consulta.filter_by(modulo_id=modulo.id)
    if rol_id is not None:
        rol = get_rol(database, rol_id)
        consulta = consulta.filter_by(rol_id=rol.id)
    return consulta.filter_by(estatus="A").order_by(Permiso.id.desc())


def get_permiso(database: Session, permiso_id: int) -> Permiso:
    """Consultar un permiso por su id"""
    permiso = database.query(Permiso).get(permiso_id)
    if permiso is None:
        raise MyNotExistsError("No existe ese permiso")
    if permiso.estatus != "A":
        raise MyIsDeletedError("No es activo ese permiso, está eliminado")
    return permiso


@permisos.get("", response_model=CustomPage[PermisoOut])
async def paginado_permisos(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    modulo_id: int = None,
    rol_id: int = None,
):
    """Paginado de permisos"""
    if current_user.permissions.get("PERMISOS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        resultados = get_permisos(
            database=database,
            modulo_id=modulo_id,
            rol_id=rol_id,
        )
    except MyAnyError as error:
        return CustomPage(success=False, message=str(error))
    return paginate(resultados)


@permisos.get("/{permiso_id}", response_model=OnePermisoOut)
async def detalle_permiso(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    permiso_id: int,
):
    """Detalle de una permisos a partir de su id"""
    if current_user.permissions.get("PERMISOS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        permiso = get_permiso(database, permiso_id)
    except MyAnyError as error:
        return OnePermisoOut(success=False, message=str(error))
    return OnePermisoOut.model_validate(permiso)
