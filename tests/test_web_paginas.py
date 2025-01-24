"""
Unit tests for sitio web category
"""

import unittest

import requests

from tests.load_env import config


class TestSitioWeb(unittest.TestCase):
    """Tests for sitio web category"""

    def test_get_web_paginas(self):
        """Test GET method for paginas"""
        try:
            response = requests.get(
                f"{config['api_base_url']}/web_paginas",
                headers={"X-Api-Key": config["api_key"]},
                timeout=config["timeout"],
            )
        except requests.exceptions.ConnectionError as error:
            self.fail(error)
        self.assertEqual(response.status_code, 200)
        contenido = response.json()
        self.assertEqual("success" in contenido, True)
        self.assertEqual("message" in contenido, True)
        self.assertEqual("total" in contenido, True)
        self.assertEqual("items" in contenido, True)
        for item in contenido["items"]:
            self.assertEqual("clave" in item, True)
            self.assertEqual("titulo" in item, True)
            self.assertEqual("resumen" in item, True)
            self.assertEqual("ruta" in item, True)
            self.assertEqual("fecha_modificacion" in item, True)
            self.assertEqual("responsable" in item, True)
            self.assertEqual("etiquetas" in item, True)
            self.assertEqual("vista_previa" in item, True)
            self.assertEqual("estado" in item, True)

    def test_get_web_pagina_by_clave(self):
        """Test GET method for pagina by clave"""
        for clave in ["AC20241004", "CN20231019", "NT20240808", "SEPTSJ202431SO"]:
            try:
                response = requests.get(
                    f"{config['api_base_url']}/web_paginas/{clave}",
                    headers={"X-Api-Key": config["api_key"]},
                    timeout=config["timeout"],
                )
            except requests.exceptions.ConnectionError as error:
                self.fail(error)
            self.assertEqual(response.status_code, 200)
            contenido = response.json()
            self.assertEqual("success" in contenido, True)
            self.assertEqual("message" in contenido, True)
            self.assertEqual("clave" in contenido, True)
            self.assertEqual(contenido["clave"] == clave, True)
            self.assertEqual("titulo" in contenido, True)
            self.assertEqual("resumen" in contenido, True)
            self.assertEqual("ruta" in contenido, True)
            self.assertEqual("fecha_modificacion" in contenido, True)
            self.assertEqual("responsable" in contenido, True)
            self.assertEqual("etiquetas" in contenido, True)
            self.assertEqual("vista_previa" in contenido, True)
            self.assertEqual("estado" in contenido, True)
            self.assertEqual("contenido" in contenido, True)


if __name__ == "__main__":
    unittest.main()
