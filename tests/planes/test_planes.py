import json
import uuid
import pytest
import logging
from unittest.mock import patch, MagicMock

from faker import Faker
from src.main import app
from src.models.db import db_session
from src.models.deportista import Deportista
from src.models.plan import Plan
from src.models.plan_deportista import PlanDeportista


fake = Faker()
logger = logging.getLogger(__name__)


@pytest.fixture(scope="class")
def setup_data():
    logger.info("Inicio TestPlanes")

    with db_session() as session:
        # Crear plan
        plan = {
            'nombre': fake.name(),
            'descripcion': fake.name(),
            'vo2': fake.random_int(min=1, max=70)
        }
        plan_random: Plan = Plan(**plan)
        session.add(plan_random)
        session.commit()
        logger.info('Plan creado: ' + plan_random.nombre)

        # Crear deportista
        deportista = {
            'nombre': fake.name(),
            'apellido': fake.name(),
            'tipo_identificacion': 'cedula_ciudadania',
            'numero_identificacion': fake.random_int(min=100000000, max=999999999),
            'email': fake.email(),
            'genero': 'masculino',
            'edad': fake.random_int(min=18, max=60),
            'peso': fake.random_int(min=50, max=100),
            'altura': fake.random_int(min=150, max=200),
            'pais_nacimiento': 'Colombia',
            'ciudad_nacimiento': 'Bogota',
            'pais_residencia': 'Colombia',
            'ciudad_residencia': 'Bogota',
            'antiguedad_residencia': fake.random_int(min=1, max=10),
            'contrasena': fake.password(),
        }
        deportista_random: Deportista = Deportista(**deportista)
        session.add(deportista_random)
        session.commit()
        logger.info('Deportista creado: ' + deportista_random.email)

        # Crear plan deportista
        plan_deportista = {
            'id_deportista': deportista_random.id,
            'id_plan': plan_random.id,
        }
        plan_deportista_random: PlanDeportista = PlanDeportista(
            **plan_deportista)
        session.add(plan_deportista_random)
        session.commit()
        logger.info('Plan deportista creado: ' +
                    str(plan_deportista_random.id))

        yield {
            'plan_id': plan_random.id,
            'deportista_email': deportista_random.email,
            'deportista_id': deportista_random.id,
            'id_plan_deportista_random': plan_deportista_random.id,
        }

        logger.info("Fin TestPlanes")
        session.delete(plan_deportista_random)
        session.delete(deportista_random)
        session.delete(plan_random)
        session.commit()


@pytest.mark.usefixtures("setup_data")
class TestPlanes():

    @patch('requests.post')
    def test_obtener_planes_deportivos(self, mock_post):
        with app.test_client() as test_client:
            deporte_id = uuid.uuid4()
            ejercicio_id = uuid.uuid4()

            deporte = {
                "deporte_id": deporte_id,
                "deporte_nombre": "Atletismo",
                "ejercicio_descripcion": "Sesión de recuperación ligera",
                "ejercicio_duracion": 30,
                "ejercicio_id": str(ejercicio_id),
                "ejercicio_nombre": fake.name(),
            }

            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = {'result': [deporte]}
            mock_post.return_value = mock_response

            response = test_client.get(
                '/gestor-usuarios/planes/obtener_planes_deportivos')
            response_json = json.loads(response.data)

            assert response.status_code == 200
            assert len(response_json) > 0

    @patch('requests.post')
    def test_obtener_planes_deportista(self, mock_post, setup_data):
        with app.test_client() as test_client:
            deportista_email = setup_data['deportista_email']

            mock_response_1 = MagicMock()
            mock_response_1.status_code = 200
            mock_response_1.json.return_value = {
                'token_valido': True, 'email': deportista_email}
            mock_response_1.return_value = mock_response_1

            plan_deportivo = {
                "deporte_id": "730e0a96-7232-4377-a65c-71e33b818fe1",
                "deporte_nombre": "Ciclismo",
                "ejercicio_descripcion": "Mejora resistencia y fuerza en piernas.",
                "ejercicio_duracion": 20,
                "ejercicio_id": "28e9a795-afd4-488d-ad28-242d7e723b5e",
                "ejercicio_nombre": "Pedaleo en Resistencia"
            }
            mock_response_2 = MagicMock()
            mock_response_2.status_code = 200
            mock_response_2.json.return_value = {'result': [plan_deportivo]}
            mock_response_2.return_value = mock_response_2

            mock_post.side_effect = [mock_response_1, mock_response_2]

            headers = {'Authorization': 'Bearer 123'}
            response = test_client.get(
                '/gestor-usuarios/planes/obtener_planes_deportista', headers=headers, follow_redirects=True)
            response_json = json.loads(response.data)
            logger.info(str(response_json))

            assert response.status_code == 200
            assert len(response_json) > 0
            assert 'alimentos' in response_json[0]
            assert 'ejercicios' in response_json[0]

    @patch('requests.post')
    def test_agregar_plan_deportivo(self, mock_post, setup_data):
        with app.test_client() as test_client:
            deportista_email = setup_data['deportista_email']
            plan = {
                'nombre': fake.name(),
                'descripcion': fake.name(),
                'vo2': fake.random_int(min=1, max=70)
            }
            plan_random: Plan = Plan(**plan)
            db_session.add(plan_random)
            db_session.commit()

            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                'token_valido': True, 'email': deportista_email}
            mock_post.return_value = mock_response

            headers = {'Authorization': 'Bearer 123'}
            body = {
                'id_plan': plan_random.id,
            }
            response = test_client.post(
                '/gestor-usuarios/planes/agregar_plan_deportivo', headers=headers, json=body, follow_redirects=True)
            response_json = json.loads(response.data)

            assert response.status_code == 200
            assert 'id_plan_deportista' in response_json

            plan_deportista = PlanDeportista.query.filter_by(
                id=response_json['id_plan_deportista']).first()

            db_session.delete(plan_deportista)
            db_session.delete(plan_random)
            db_session.commit()

    @patch('requests.post')
    def test_agregar_plan_deportivo_sin_email(self, mock_post, setup_data):
        with app.test_client() as test_client:
            plan_id = setup_data['plan_id']

            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                'token_valido': True, 'email': None}
            mock_post.return_value = mock_response

            headers = {'Authorization': 'Bearer 123'}
            body = {
                'id_plan': plan_id,
            }
            response = test_client.post(
                '/gestor-usuarios/planes/agregar_plan_deportivo', headers=headers, json=body, follow_redirects=True)

            assert response.status_code == 400

    @patch('requests.post')
    def test_agregar_plan_deportivo_sin_id_plan(self, mock_post, setup_data):
        with app.test_client() as test_client:
            deportista_email = setup_data['deportista_email']

            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                'token_valido': True, 'email': deportista_email}
            mock_post.return_value = mock_response

            headers = {'Authorization': 'Bearer 123'}
            body = {
                'id_plan': None,
            }
            response = test_client.post(
                '/gestor-usuarios/planes/agregar_plan_deportivo', headers=headers, json=body, follow_redirects=True)

            assert response.status_code == 400

    @patch('requests.post')
    def test_obtener_ejercicios_plan_deportista(self, mock_post, setup_data):
        with app.test_client() as test_client:
            deportista_email = setup_data['deportista_email']
            deportista_id = setup_data['deportista_id']

            plan_deportista: PlanDeportista = PlanDeportista.query.filter_by(
                id_deportista=deportista_id).first()

            mock_response_1 = MagicMock()
            mock_response_1.status_code = 200
            mock_response_1.json.return_value = {
                'token_valido': True, 'email': deportista_email}
            mock_response_1.return_value = mock_response_1

            plan_deportivo = {
                "deporte_id": "730e0a96-7232-4377-a65c-71e33b818fe1",
                "deporte_nombre": "Ciclismo",
                "ejercicio_descripcion": "Mejora resistencia y fuerza en piernas.",
                "ejercicio_duracion": 20,
                "ejercicio_id": "28e9a795-afd4-488d-ad28-242d7e723b5e",
                "ejercicio_nombre": "Pedaleo en Resistencia"
            }
            mock_response_2 = MagicMock()
            mock_response_2.status_code = 200
            mock_response_2.json.return_value = {'result': [plan_deportivo]}
            mock_response_2.return_value = mock_response_2

            mock_post.side_effect = [mock_response_1, mock_response_2]

            headers = {'Authorization': 'Bearer 123'}
            response = test_client.get(
                f'/gestor-usuarios/planes/obtener_ejercicios_plan_deportista/{plan_deportista.id_plan}/123456', headers=headers, follow_redirects=True)
            response_json = json.loads(response.data)

            assert response.status_code == 200
            assert len(response_json) > 0
            assert 'ejercicios' in response_json

    def test_obtener_ejercicios_plan_deportista_sin_token(self):
        with app.test_client() as test_client:
            response = test_client.get(
                '/gestor-usuarios/planes/obtener_ejercicios_plan_deportista/123/123456', follow_redirects=True)

            assert response.status_code == 403

    def test_obtener_alimentos_plan_sin_id_plan(self):
        with app.test_client() as test_client:
            response = test_client.get(
                '/gestor-usuarios/planes/obtener_alimentos_plan/', follow_redirects=True)

            assert response.status_code == 404

    def test_obtener_alimentos_plan_no_existe(self):
        with app.test_client() as test_client:
            uuid_rnd = uuid.uuid4()

            response = test_client.get(
                f'/gestor-usuarios/planes/obtener_alimentos_plan/{uuid_rnd}', follow_redirects=True)
            response_json = json.loads(response.data)

            assert response.status_code == 200
            assert 'alimentos' in response_json

    def test_obtener_alimentos_plan_exitoso(self, setup_data):
        with app.test_client() as test_client:
            id_plan_deportista = setup_data['id_plan_deportista_random']

            response = test_client.get(
                f'/gestor-usuarios/planes/obtener_alimentos_plan/{id_plan_deportista}', follow_redirects=True)
            response_json = json.loads(response.data)

            assert response.status_code == 200
            assert 'alimentos' in response_json
