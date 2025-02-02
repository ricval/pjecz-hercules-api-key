"""
Roles
"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate

from ..dependencies.authentications import UsuarioInDB, get_current_active_user
from ..dependencies.database import Session, get_db
from ..dependencies.fastapi_pagination_custom_page import CustomPage
from ..models.permisos import Permiso
from ..models.roles import Rol
from ..schemas.roles import RolOut

roles = APIRouter(prefix="/api/v5/roles", tags=["usuarios"])


@roles.get("", response_model=CustomPage[RolOut])
async def paginado_roles(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
):
    """Paginado de roles"""
    if current_user.permissions.get("ROLES", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    return paginate(database.query(Rol).filter_by(estatus="A").order_by(Rol.nombre))
