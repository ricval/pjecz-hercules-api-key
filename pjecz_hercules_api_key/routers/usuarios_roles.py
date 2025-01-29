"""
Usuarios-Roles v4, rutas (paths)
"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound

from ..dependencies.authentications import UsuarioInDB, get_current_active_user
from ..dependencies.database import Session, get_db
from ..dependencies.fastapi_pagination_custom_page import CustomPage
from ..dependencies.safe_string import safe_email
from ..models.permisos import Permiso
from ..models.roles import Rol
from ..models.usuarios import Usuario
from ..models.usuarios_roles import UsuarioRol
from ..schemas.usuarios_roles import OneUsuarioRolOut, UsuarioRolOut

usuarios_roles = APIRouter(prefix="/v4/usuarios_roles", tags=["usuarios"])


@usuarios_roles.get("/{usuario_rol_id}", response_model=OneUsuarioRolOut)
async def detalle_usuario_rol(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    usuario_rol_id: int,
):
    """Detalle de una usuarios-roles a partir de su id"""
    if current_user.permissions.get("USUARIOS ROLES", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    usuario_rol = database.query(UsuarioRol).get(usuario_rol_id)
    if usuario_rol is None:
        return OneUsuarioRolOut(success=False, message="No existe ese usuario-rol")
    if usuario_rol.estatus != "A":
        return OneUsuarioRolOut(success=False, message="No es activo ese usuario-rol, está eliminado")
    return OneUsuarioRolOut.model_validate(usuario_rol)


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
        rol = database.query(Rol).get(rol_id)
        if rol is None:
            return CustomPage(success=False, message="No existe ese rol")
        if rol.estatus != "A":
            return CustomPage(success=False, message="No es activo ese rol, está eliminado")
        consulta = consulta.filter_by(rol_id=rol.id)
    if email is not None:
        try:
            email = safe_email(email)
        except ValueError:
            return CustomPage(success=False, message="El email no es válido")
        try:
            usuario = database.query(Usuario).filter_by(email=email).filter_by(estatus="A").one()
        except (MultipleResultsFound, NoResultFound):
            return CustomPage(success=False, message="No existe ese usuario o está eliminado")
        consulta = consulta.filter_by(usuario_id=usuario.id)
    return paginate(consulta.filter_by(estatus="A").order_by(UsuarioRol.id.desc()))
