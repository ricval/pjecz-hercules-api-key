"""
Usuarios v4, rutas (paths)
"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound

from ..dependencies.authentications import UsuarioInDB, get_current_active_user
from ..dependencies.database import Session, get_db
from ..dependencies.fastapi_pagination_custom_page import CustomPage
from ..dependencies.safe_string import safe_email, safe_string
from ..models.permisos import Permiso
from ..models.usuarios import Usuario
from ..schemas.usuarios import OneUsuarioOut, UsuarioOut

usuarios = APIRouter(prefix="/v4/usuarios", tags=["usuarios"])


@usuarios.get("/{email}", response_model=OneUsuarioOut)
async def detalle_usuario(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    email: str,
):
    """Detalle de una usuarios a partir de su e-mail"""
    if current_user.permissions.get("USUARIOS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        email = safe_email(email)
    except ValueError:
        return OneUsuarioOut(success=False, message="El email no es válido")
    try:
        usuario = database.query(Usuario).filter_by(email=email).one()
    except (MultipleResultsFound, NoResultFound):
        return OneUsuarioOut(success=False, message="No existe ese usuario")
    if usuario.estatus != "A":
        return OneUsuarioOut(success=False, message="No es activo ese usuario, está eliminado")
    return OneUsuarioOut.model_validate(usuario)


@usuarios.get("", response_model=CustomPage[UsuarioOut])
async def paginado_usuarios(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    apellido_paterno: str = None,
    apellido_materno: str = None,
    email: str = None,
    nombres: str = None,
):
    """Paginado de usuarios"""
    if current_user.permissions.get("USUARIOS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    consulta = database.query(Usuario)
    if apellido_paterno is not None:
        apellido_paterno = safe_string(apellido_paterno)
        if apellido_paterno != "":
            consulta = consulta.filter(Usuario.apellido_paterno.contains(apellido_paterno))
    if apellido_materno is not None:
        apellido_materno = safe_string(apellido_materno)
        if apellido_materno != "":
            consulta = consulta.filter(Usuario.apellido_materno.contains(apellido_materno))
    if email is not None:
        try:
            email = safe_email(email, search_fragment=True)
        except ValueError:
            return CustomPage(success=False, message="El email no es válido")
        consulta = consulta.filter(Usuario.email.contains(email))
    if nombres is not None:
        nombres = safe_string(nombres)
        if nombres != "":
            consulta = consulta.filter(Usuario.nombres.contains(nombres))
    return paginate(consulta.filter_by(estatus="A").order_by(Usuario.email))
