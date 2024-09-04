"""
Unit tests for sitio web category
"""

import unittest

import requests

from tests.load_env import config


class TestSitioWeb(unittest.TestCase):
    """Tests for sitio web category"""

    def test_get_web_ramas(self):
        """Test GET method for ramas"""
        response = requests.get(
            f"{config['api_base_url']}/web_ramas",
            headers={"X-Api-Key": config["api_key"]},
            timeout=config["timeout"],
        )
        self.assertEqual(response.status_code, 200)

    def test_get_web_rama_by_clave(self):
        """Test GET method for rama by clave"""
        for clave in ["AC", "CO", "EN", "NO", "OJ", "SE", "TR"]:
            response = requests.get(
                f"{config['api_base_url']}/web_ramas/{clave}",
                headers={"X-Api-Key": config["api_key"]},
                timeout=config["timeout"],
            )
            self.assertEqual(response.status_code, 200)

    def test_get_web_paginas(self):
        """Test GET method for paginas"""
        response = requests.get(
            f"{config['api_base_url']}/web_paginas",
            headers={"X-Api-Key": config["api_key"]},
            timeout=config["timeout"],
        )
        self.assertEqual(response.status_code, 200)

    def test_get_web_pagina_by_clave(self):
        """Test GET method for pagina by clave"""
        for clave in ["OJ", "OJA", "OJBD", "OJI", "OJQS", "OJR"]:
            response = requests.get(
                f"{config['api_base_url']}/web_paginas/{clave}",
                headers={"X-Api-Key": config["api_key"]},
                timeout=config["timeout"],
            )
            self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
