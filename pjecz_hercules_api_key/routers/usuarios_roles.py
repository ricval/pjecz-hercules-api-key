"""
Usuarios-Roles v4
"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate

from ..dependencies.authentications import UsuarioInDB, get_current_active_user
from ..dependencies.database import Session, get_db
from ..dependencies.fastapi_pagination_custom_page import CustomPage
from ..dependencies.safe_string import safe_email
from ..models.permisos import Permiso
from ..models.roles import Rol
from ..models.usuarios import Usuario
from ..models.usuarios_roles import UsuarioRol
from ..schemas.usuarios_roles import UsuarioRolOut

usuarios_roles = APIRouter(prefix="/api/v5/usuarios_roles", tags=["usuarios"])


@usuarios_roles.get("", response_model=CustomPage[UsuarioRolOut])
async def paginado_usuarios_roles(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    rol_id: int = None,
    email: str = None,
):
    """Paginado de usuarios-roles"""
    if current_user.permissions.get("USUARIOS ROLES", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    consulta = database.query(UsuarioRol)
    if rol_id is not None:
        consulta = consulta.join(Rol).filter(Rol.id == rol_id).filter(Rol.estatus == "A")
    if email is not None:
        try:
            email = safe_email(email)
        except ValueError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No es válido el e-mail")
        consulta = consulta.join(Usuario).filter(Usuario.email == email).filter(Usuario.estatus == "A")
    return paginate(consulta.filter(UsuarioRol.estatus == "A").order_by(UsuarioRol.id.desc()))
