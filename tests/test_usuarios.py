"""
Unit tests for usuarios category
"""

import unittest

import requests

from tests.load_env import config


class TestUsuarios(unittest.TestCase):
    """Tests for usuarios category"""

    def test_get_modulos(self):
        """Test GET method for modulos"""
        response = requests.get(
            f"{config['api_base_url']}/modulos",
            headers={"X-Api-Key": config["api_key"]},
            timeout=config["timeout"],
        )
        self.assertEqual(response.status_code, 200)

    def test_get_permisos(self):
        """Test GET method for permisos"""
        response = requests.get(
            f"{config['api_base_url']}/permisos",
            headers={"X-Api-Key": config["api_key"]},
            timeout=config["timeout"],
        )
        self.assertEqual(response.status_code, 200)

    def test_get_roles(self):
        """Test GET method for roles"""
        response = requests.get(
            f"{config['api_base_url']}/roles",
            headers={"X-Api-Key": config["api_key"]},
            timeout=config["timeout"],
        )
        self.assertEqual(response.status_code, 200)

    def test_get_usuarios(self):
        """Test GET method for usuarios"""
        response = requests.get(
            f"{config['api_base_url']}/usuarios",
            headers={"X-Api-Key": config["api_key"]},
            timeout=config["timeout"],
        )
        self.assertEqual(response.status_code, 200)

    def test_get_usuarios_roles(self):
        """Test GET method for usuarios_roles"""
        response = requests.get(
            f"{config['api_base_url']}/usuarios_roles",
            headers={"X-Api-Key": config["api_key"]},
            timeout=config["timeout"],
        )
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
