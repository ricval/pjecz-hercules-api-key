"""
Permisos
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
from ..schemas.permisos import PermisoOut

permisos = APIRouter(prefix="/api/v5/permisos", tags=["usuarios"])


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
        consulta = consulta.join(Modulo).filter(Modulo.id == modulo_id).filter(Modulo.estatus == "A")
    if rol_id is not None:
        consulta = consulta.join(Rol).filter(Rol.id == rol_id).filter(Rol.estatus == "A")
    return paginate(consulta.filter(Permiso.estatus == "A").order_by(Permiso.id.desc()))
