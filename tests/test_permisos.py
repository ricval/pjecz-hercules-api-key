"""
Unit tests for permisos
"""

import unittest

import requests

from tests import config


class TestPermisos(unittest.TestCase):
    """Tests for permisos"""

    def test_get_permisos(self):
        """Test GET method for permisos"""

        # Consultar permisos
        try:
            response = requests.get(
                f"{config['api_base_url']}/api/v5/permisos",
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


if __name__ == "__main__":
    unittest.main()
