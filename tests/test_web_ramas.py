"""
Unit tests for web ramas
"""

import unittest

import requests

from tests import config


class TestSitioWeb(unittest.TestCase):
    """Tests for web ramas"""

    def test_get_web_ramas(self):
        """Test GET method for ramas"""

        # Consultar web ramas
        try:
            response = requests.get(
                f"{config['api_base_url']}/api/v5/web_ramas",
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

        # Validar que en los datos haya el listado de autoridades
        self.assertEqual(type(contenido["data"]), list)
        # self.assertEqual("clave" in item, True)
        # self.assertEqual("nombre" in item, True)

    def test_get_web_rama_by_clave(self):
        """Test GET method for rama by clave"""

        # Bucle por claves de ramas
        for clave in ["AC", "CO", "EN", "OJ", "SE", "TR"]:
            # Consultar rama por clave
            try:
                response = requests.get(
                    f"{config['api_base_url']}/api/v5/web_ramas/{clave}",
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
            # self.assertEqual(type(contenido["data"]), list)
            # self.assertEqual(contenido["clave"] == clave, True)
            # self.assertEqual("nombre" in contenido, True)


if __name__ == "__main__":
    unittest.main()
