"""
Sentencias
"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound

from ..dependencies.authentications import UsuarioInDB, get_current_active_user
from ..dependencies.database import Session, get_db
from ..dependencies.fastapi_pagination_custom_page import CustomPage
from ..dependencies.safe_string import safe_clave
from ..models.autoridades import Autoridad
from ..models.permisos import Permiso
from ..models.sentencias import Sentencia
from ..schemas.sentencias import OneSentenciaOut, SentenciaOut

sentencias = APIRouter(prefix="/api/v5/sentencias", tags=["sentencias"])
