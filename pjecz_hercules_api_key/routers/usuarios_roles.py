"""
Usuarios-Roles v4, rutas (paths)
"""

from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate

from ..dependencies.authentications import UsuarioInDB, get_current_active_user
from ..dependencies.database import Session, get_db
from ..dependencies.exceptions import MyAnyError, MyIsDeletedError, MyNotExistsError
from ..dependencies.fastapi_pagination_custom_page import CustomPage
from ..models.permisos import Permiso
from ..models.usuarios_roles import UsuarioRol
from ..schemas.usuarios_roles import OneUsuarioRolOut, UsuarioRolOut
from .roles import get_rol, get_rol_with_nombre
from .usuarios import get_usuario, get_usuario_with_email

usuarios_roles = APIRouter(prefix="/v4/usuarios_roles", tags=["usuarios"])


def get_usuarios_roles(
    database: Session,
    rol_id: int = None,
    rol_nombre: str = None,
    usuario_id: int = None,
    usuario_email: str = None,
) -> Any:
    """Consultar los usuarios-roles activos"""
    consulta = database.query(UsuarioRol)
    if rol_id is not None:
        rol = get_rol(database, rol_id)
        consulta = consulta.filter_by(rol_id == rol.id)
    if rol_nombre is not None:
        rol = get_rol_with_nombre(database, rol_nombre)
        consulta = consulta.filter_by(rol_id == rol.id)
    if usuario_id is not None:
        usuario = get_usuario(database, usuario_id)
        consulta = consulta.filter_by(usuario_id == usuario.id)
    if usuario_email is not None:
        usuario = get_usuario_with_email(database, usuario_email)
        consulta = consulta.filter_by(usuario_id == usuario.id)
    return consulta.filter_by(estatus="A").order_by(UsuarioRol.id.desc())


def get_usuario_rol(database: Session, usuario_rol_id: int) -> UsuarioRol:
    """Consultar un usuario-rol por su id"""
    usuario_rol = database.query(UsuarioRol).get(usuario_rol_id)
    if usuario_rol is None:
        raise MyNotExistsError("No existe ese usuario-rol")
    if usuario_rol.estatus != "A":
        raise MyIsDeletedError("No es activo ese usuario-rol, está eliminado")
    return usuario_rol


@usuarios_roles.get("", response_model=CustomPage[UsuarioRolOut])
async def paginado_usuarios_roles(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    rol_id: int = None,
    rol_nombre: str = None,
    usuario_id: int = None,
    usuario_email: str = None,
):
    """Paginado de usuarios-roles"""
    if current_user.permissions.get("USUARIOS ROLES", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        resultados = get_usuarios_roles(
            database=database,
            rol_id=rol_id,
            rol_nombre=rol_nombre,
            usuario_id=usuario_id,
            usuario_email=usuario_email,
        )
    except MyAnyError as error:
        return CustomPage(success=False, message=str(error))
    return paginate(resultados)


@usuarios_roles.get("/{usuario_rol_id}", response_model=OneUsuarioRolOut)
async def detalle_usuario_rol(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    usuario_rol_id: int,
):
    """Detalle de una usuarios-roles a partir de su id"""
    if current_user.permissions.get("USUARIOS ROLES", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        usuario_rol = get_usuario_rol(database, usuario_rol_id)
    except MyAnyError as error:
        return OneUsuarioRolOut(success=False, message=str(error))
    return OneUsuarioRolOut.model_validate(usuario_rol)
