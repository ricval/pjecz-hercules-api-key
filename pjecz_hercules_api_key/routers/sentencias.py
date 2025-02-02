"""
Sentencias
"""

from datetime import date, datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate

from ..dependencies.authentications import UsuarioInDB, get_current_active_user
from ..dependencies.database import Session, get_db
from ..dependencies.fastapi_pagination_custom_page import CustomPage
from ..dependencies.safe_string import safe_clave
from ..models.autoridades import Autoridad
from ..models.materias_tipos_juicios import MateriaTipoJuicio
from ..models.permisos import Permiso
from ..models.sentencias import Sentencia
from ..schemas.sentencias import OneSentenciaOut, SentenciaOut, SentenciaRAGOut

sentencias = APIRouter(prefix="/api/v5/sentencias", tags=["sentencias"])


@sentencias.get("/{sentencia_id}", response_model=OneSentenciaOut)
async def detalle(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    sentencia_id: int,
):
    """Detalle de una sentencia a partir de su ID"""
    if current_user.permissions.get("SENTENCIAS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    sentencia = database.query(Sentencia).get(sentencia_id)
    if sentencia is None:
        return OneSentenciaOut(success=False, message="No existe esa sentencia")
    if sentencia.estatus != "A":
        return OneSentenciaOut(success=False, message="No es activa esa sentencia, está eliminada")
    return OneSentenciaOut(success=True, message="Detalle de una sentencia", data=SentenciaRAGOut.model_validate(sentencia))


@sentencias.get("", response_model=CustomPage[SentenciaOut])
async def paginado(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    autoridad_clave: str = None,
    creado: date = None,
    creado_desde: date = None,
    creado_hasta: date = None,
    materia_tipo_juicio_id: int = None,
):
    """Paginado de sentencias"""
    if current_user.permissions.get("SENTENCIAS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    consulta = database.query(Sentencia)
    if autoridad_clave is not None:
        try:
            autoridad_clave = safe_clave(autoridad_clave)
        except ValueError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No es válida la clave")
        consulta = consulta.join(Autoridad).filter(Autoridad.clave == autoridad_clave).filter(Autoridad.estatus == "A")
    if creado is not None:
        consulta = consulta.filter(Sentencia.creado >= datetime(creado.year, creado.month, creado.day, 0, 0, 0))
        consulta = consulta.filter(Sentencia.creado <= datetime(creado.year, creado.month, creado.day, 23, 59, 59))
    else:
        if creado_desde is not None:
            consulta = consulta.filter(
                Sentencia.creado >= datetime(creado_desde.year, creado_desde.month, creado_desde.day, 0, 0, 0)
            )
        if creado_hasta is not None:
            consulta = consulta.filter(
                Sentencia.creado <= datetime(creado_hasta.year, creado_hasta.month, creado_hasta.day, 23, 59, 59)
            )
    if materia_tipo_juicio_id is not None:
        consulta = (
            consulta.join(MateriaTipoJuicio)
            .filter(MateriaTipoJuicio.id == materia_tipo_juicio_id)
            .filter(MateriaTipoJuicio.estatus == "A")
        )
    return paginate(consulta.filter(Sentencia.estatus == "A").order_by(Sentencia.id.desc()))
