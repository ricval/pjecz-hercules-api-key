"""
Unit tests for usuarios-roles
"""

import unittest

import requests

from tests import config


class TestUsuariosRoles(unittest.TestCase):
    """Tests for usuarios-roles"""

    def test_get_usuarios_roles(self):
        """Test GET method for usuarios_roles"""

        # Consultar usuarios-roles
        try:
            response = requests.get(
                f"{config['api_base_url']}/api/v5/usuarios_roles",
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
