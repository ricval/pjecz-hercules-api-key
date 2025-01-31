"""
Tests Init
"""

import os

from dotenv import load_dotenv

load_dotenv()


# Cargar las variables de entorno
config = {
    "api_key": os.getenv("API_KEY", ""),
    "api_base_url": os.getenv("API_BASE_URL", "http://127.0.0.1:8000"),
    "timeout": int(os.getenv("TIMEOUT", "10")),
    "usuario_email": os.getenv("USUARIO_EMAIL", "anonymous@server.com"),
    "web_paginas_claves": os.getenv("WEB_PAGINAS_CLAVES", "TEST1,TEST2,TEST3").split(","),
    "web_ramas_claves": os.getenv("WEB_RAMAS_CLAVES", "TEST1,TEST2,TEST3").split(","),
}
