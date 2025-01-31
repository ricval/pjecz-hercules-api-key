"""
Unit tests for web paginas
"""

import unittest

import requests

from tests import config


class TestSitioWeb(unittest.TestCase):
    """Tests for web paginas"""

    def test_get_web_paginas(self):
        """Test GET method for web paginas"""

        # Consultar
        try:
            response = requests.get(
                f"{config['api_base_url']}/api/v5/web_paginas",
                headers={"X-Api-Key": config["api_key"]},
                timeout=config["timeout"],
            )
        except requests.exceptions.RequestException as error:
            self.fail(error)
        self.assertEqual(response.status_code, 200)

        # Validar el contenido de la respuesta
        contenido = response.json()
        self.assertEqual("success" in contenido, True)
        self.assertEqual("message" in contenido, True)
        self.assertEqual("data" in contenido, True)

        # Validar que se haya tenido éxito
        self.assertEqual(contenido["success"], True)

        # Validar los datos
        self.assertEqual(type(contenido["data"]), list)
        for item in contenido["data"]:
            self.assertEqual("clave" in item, True)
            self.assertEqual("contenido" in item, True)
            self.assertEqual("etiquetas" in item, True)
            self.assertEqual("estado" in item, True)
            self.assertEqual("fecha_modificacion" in item, True)
            self.assertEqual("responsable" in item, True)
            self.assertEqual("resumen" in item, True)
            self.assertEqual("ruta" in item, True)
            self.assertEqual("titulo" in item, True)
            self.assertEqual("vista_previa" in item, True)

    def test_get_web_pagina_by_clave(self):
        """Test GET method for web pagina by clave"""

        # Bucle por claves
        for clave in config["web_paginas_claves"]:
            # Consultar
            try:
                response = requests.get(
                    f"{config['api_base_url']}/api/v5/web_paginas/{clave}",
                    headers={"X-Api-Key": config["api_key"]},
                    timeout=config["timeout"],
                )
            except requests.exceptions.ConnectionError as error:
                self.fail(error)
            self.assertEqual(response.status_code, 200)

            # Validar el contenido de la respuesta
            contenido = response.json()
            self.assertEqual("success" in contenido, True)
            self.assertEqual("message" in contenido, True)
            self.assertEqual("data" in contenido, True)

            # Validar que se haya tenido éxito
            self.assertEqual(contenido["success"], True)

            # Validar los datos
            self.assertEqual(type(contenido["data"]), dict)
            item = contenido["data"]
            self.assertEqual("clave" in item, True)
            self.assertEqual(item["clave"] == clave, True)
            self.assertEqual("contenido" in item, True)
            self.assertEqual("etiquetas" in item, True)
            self.assertEqual("estado" in item, True)
            self.assertEqual("fecha_modificacion" in item, True)
            self.assertEqual("responsable" in item, True)
            self.assertEqual("resumen" in item, True)
            self.assertEqual("ruta" in item, True)
            self.assertEqual("titulo" in item, True)
            self.assertEqual("vista_previa" in item, True)


if __name__ == "__main__":
    unittest.main()
