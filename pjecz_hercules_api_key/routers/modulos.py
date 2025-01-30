"""
Modulos v4
"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate

from ..dependencies.authentications import UsuarioInDB, get_current_active_user
from ..dependencies.database import Session, get_db
from ..dependencies.fastapi_pagination_custom_page import CustomPage
from ..models.modulos import Modulo
from ..models.permisos import Permiso
from ..schemas.modulos import ModuloOut

modulos = APIRouter(prefix="/v4/modulos", tags=["usuarios"])


@modulos.get("", response_model=CustomPage[ModuloOut])
async def paginado_modulos(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
):
    """Paginado de módulos"""
    if current_user.permissions.get("MODULOS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    return paginate(database.query(Modulo).filter_by(estatus="A").order_by(Modulo.nombre))
