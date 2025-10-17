"""
Unit tests for exh_exhortos
"""

import unittest
import json

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
        # Definir si es una persona moral o física
        es_persona_moral = faker.random_element(elements=(True, False))
        if es_persona_moral:
            parte_demandado = {
                "es_persona_moral": True,
                "nombre": faker.company(),
                "tipo_parte": 2,  # 2 es demandado
            }
        else:
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

        # Definir los archivos
        archivos = []
        num_archivos = faker.random_int(min=1, max=5)
        for i in range(num_archivos):
            # Definir el archivo
            archivo = {
                "nombre_archivo": faker.file_name(),
                "tipo_documento": faker.random_int(min=1, max=3),
                "url": faker.url(),
            }
            archivos.append(archivo)

        # Definir valores random para los campos de un exhorto
        # Definir la materia
        # Consultar materias que tengan acceso a exhortos
        materia = ""
        try:
            respuesta_materia = requests.get(
                url=f"{config['api_base_url']}/api/v5/materias",
                headers={"X-Api-Key": config["api_key"]},
                timeout=config["timeout"],
                params= {
                    "en_exh_exhortos": True
                },
            )
        except requests.exceptions.ConnectionError as error:
            self.fail(error)
        self.assertEqual(respuesta_materia.status_code, 200)
        # Extraer las claves de las materias
        contenido_materia = respuesta_materia.json()
        self.assertEqual(contenido_materia["success"], True)
        materias_data = contenido_materia["data"]
        # Extraer listado de materias
        materias = []
        for materia_data in materias_data:
            materias.append(materia_data["clave"])
        self.assertGreater(len(materias), 0)
        # Selección de la materia de forma aleatoria del listado de materias
        materia = faker.random_element(elements=materias)

        # Definir el exhorto
        exh_exhorto = {
            "autoridad_clave": "TRC-J1-FAM",
            "exh_area_clave": "TRC-OCP",
            "municipio_origen_id": 30,
            "exhorto_origen_id": str(faker.pystr(min_chars=10, max_chars=10)).upper(),
            "municipio_destino_id": 35,
            "materia_clave": materia,
            "juzgado_origen_id": "SLT-J1-FAM",
            "juzgado_origen_nombre": "JUZGADO PRIMERO DE PRIMERA INSTANCIA DEL DISTRITO JUDICIAL DE SALTILLO",
            "numero_expediente_origen": f"{faker.random_int(min=1, max=999)}/2025",
            "tipo_juicio_asunto_delitos": "DIVORCIO",
            "fojas": faker.random_int(min=1, max=99),
            "dias_responder": faker.random_int(min=1, max=31),
            # "exh_exhorto_partes": [parte_actor, parte_demandado],
            # "exh_exhorto_archivos": archivos,
            "materias": materias,
        }

        # DEBUG:
        salida = json.dumps(exh_exhorto, indent=4, ensure_ascii=False)
        print(salida)
        return None

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



if __name__ == "__main__":
    unittest.main()
