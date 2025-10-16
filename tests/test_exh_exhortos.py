"""
Unit tests for exh_exhortos
"""

import unittest

import requests
from faker import Faker

from tests import config


class TestExhExhortos(unittest.TestCase):
    """Tests for exh_exhortos"""

    def test_get_exh_exhortos(self):
        """Test GET method for exh_exhortos"""

        # Consultar
        try:
            response = requests.get(
                f"{config['api_base_url']}/api/v5/exh_exhortos",
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
            self.assertEqual("id" in item, True)
            self.assertEqual("autoridad_clave" in item, True)
            self.assertEqual("exhorto_origen_id" in item, True)

    def test_post_exh_exhortos(self):
        """Test POST method for exh_exhortos"""

        # Preparar el Faker
        faker = Faker("es_MX")

        # Definir la parte actora
        parte_actor_genero = faker.random_element(elements=("M", "F"))
        if parte_actor_genero == "M":
            parte_actor_nombre = faker.first_name_male()
            parte_actor_apellido_paterno = faker.last_name_male()
            parte_actor_apellido_materno = faker.last_name_male()
        else:
            parte_actor_nombre = faker.first_name_female()
            parte_actor_apellido_paterno = faker.last_name_female()
            parte_actor_apellido_materno = faker.last_name_female()
        parte_actor = {
            "nombre": parte_actor_nombre,
            "apellido_paterno": parte_actor_apellido_paterno,
            "apellido_materno": parte_actor_apellido_materno,
            "genero": parte_actor_genero,
            "es_persona_moral": False,
            "tipo_parte": 1,  # 1 es actora
            "tipo_parte_nombre": "",  # Va vacío porque tipo_parte NO es 3
        }

        # Definir la parte demandada
        parte_demandado_genero = faker.random_element(elements=("M", "F"))
        if parte_demandado_genero == "M":
            parte_demandado_nombre = faker.first_name_male()
            parte_demandado_apellido_paterno = faker.last_name_male()
            parte_demandado_apellido_materno = faker.last_name_male()
        else:
            parte_demandado_nombre = faker.first_name_female()
            parte_demandado_apellido_paterno = faker.last_name_female()
            parte_demandado_apellido_materno = faker.last_name_female()
        parte_demandado = {
            "nombre": parte_demandado_nombre,
            "apellido_paterno": parte_demandado_apellido_paterno,
            "apellido_materno": parte_demandado_apellido_materno,
            "genero": parte_demandado_genero,
            "es_persona_moral": False,
            "tipo_parte": 2,  # 2 es demandado
            "tipo_parte_nombre": "",  # Va vacío porque tipo_parte NO es 3
        }

        # Definir el exhorto
        exh_exhorto = {
            "autoridad_clave": "TRC-J1-FAM",
            "exh_area_clave": "TRC-OCP",
            "municipio_origen_id": 30,
            "exhorto_origen_id": "y7p5biVIxjuiw3te",
            "municipio_destino_id": 35,
            "materia_clave": "FAM",
            "juzgado_origen_id": "SLT-J1-FAM",
            "juzgado_origen_nombre": "JUZGADO PRIMERO DE PRIMERA INSTANCIA DEL DISTRITO JUDICIAL DE SALTILLO",
            "numero_expediente_origen": "1/2025",
            "tipo_juicio_asunto_delitos": "DIVORCIO",
            "fojas": 20,
            "dias_responder": 30,
            "exh_exhorto_partes": [parte_actor, parte_demandado],
        }

        # Mandar el exhorto
        try:
            respuesta = requests.post(
                url=f"{config['api_base_url']}/api/v5/exh_exhortos",
                headers={"X-Api-Key": config["api_key"]},
                timeout=config["timeout"],
                json=exh_exhorto,
            )
        except requests.exceptions.ConnectionError as error:
            self.fail(error)
        self.assertEqual(respuesta.status_code, 200)

        # Validaciones


if __name__ == "__main__":
    unittest.main()
