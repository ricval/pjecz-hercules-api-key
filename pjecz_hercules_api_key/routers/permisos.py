"""
Permisos v4, rutas (paths)
"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate

from ..dependencies.authentications import UsuarioInDB, get_current_active_user
from ..dependencies.database import Session, get_db
from ..dependencies.fastapi_pagination_custom_page import CustomPage
from ..models.modulos import Modulo
from ..models.permisos import Permiso
from ..models.roles import Rol
from ..schemas.permisos import OnePermisoOut, PermisoOut

permisos = APIRouter(prefix="/v4/permisos", tags=["usuarios"])


@permisos.get("/{permiso_id}", response_model=OnePermisoOut)
async def detalle_permiso(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    permiso_id: int,
):
    """Detalle de una permisos a partir de su id"""
    if current_user.permissions.get("PERMISOS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    permiso = database.query(Permiso).get(permiso_id)
    if permiso is None:
        return OnePermisoOut(success=False, message="No existe ese permiso")
    if permiso.estatus != "A":
        return OnePermisoOut(success=False, message="No es activo ese permiso, está eliminado")
    return OnePermisoOut.model_validate(permiso)


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
    consulta = database.query(Permiso)
    if modulo_id is not None:
        modulo = database.query(Modulo).get(modulo_id)
        if modulo is None:
            return CustomPage(success=False, message="No existe ese módulo")
        if modulo.estatus != "A":
            return CustomPage(success=False, message="No es activo ese módulo, está eliminado")
        consulta = consulta.filter_by(modulo_id=modulo.id)
    if rol_id is not None:
        rol = database.query(Rol).get(rol_id)
        if rol is None:
            return CustomPage(success=False, message="No existe ese rol")
        if rol.estatus != "A":
            return CustomPage(success=False, message="No es activo ese rol, está eliminado")
        consulta = consulta.filter_by(rol_id=rol.id)
    return paginate(consulta.filter_by(estatus="A").order_by(Permiso.id.desc()))
