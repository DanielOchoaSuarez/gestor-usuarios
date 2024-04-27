import json
import uuid
import pytest
import logging
from unittest.mock import patch, MagicMock

from faker import Faker
from src.main import app
from src.models.db import db_session
from src.models.deportista import Deportista
from src.models.perfil_deportivo import PerfilDeportivo
from src.utils.seguridad_utils import UsuarioToken


fake = Faker()
logger = logging.getLogger(__name__)


@pytest.fixture(scope="class")
def setup_data():
    logger.info("Inicio Test Perfil Deportivo")

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
    db_session.add(deportista_random)
    db_session.commit()
    logger.info('Deportista creado: ' + deportista_random.email)

    yield {
        'deportista': deportista_random,
    }

    logger.info("Fin TestPlanes")
    db_session.delete(deportista_random)
    db_session.commit()


@pytest.mark.usefixtures("setup_data")
class TestPerfilDeportivo():
    
    @patch('requests.post')
    def test_agregar_perfil_deportivo(self, mock_post, setup_data):
        with app.test_client() as test_client:
            deportista: Deportista = setup_data['deportista']

            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                'token_valido': True, 'email': deportista.email}
            mock_post.return_value = mock_response


            body = {
                'id_deportista': deportista.id,
                "FTP_actual": fake.random_int(min=50, max=100),
                "VO2max_actual": fake.random_int(min=50, max=100),
                "detalle_lesion_molestia_incapacidad": fake.text(),
                "dias_semana_practica": fake.random_int(min=1, max=7),
                "lesion_molestia_incapacidad": True,
                "tiempo_practica": fake.random_int(min=50, max=100)
            }

            headers = {'Authorization': 'Bearer 123'}

            response = test_client.post(
                '/gestor-usuarios/perfil-deportivo/agregar', headers=headers, json=body, follow_redirects=True)
            response_json = json.loads(response.data)

            assert response.status_code == 200
            assert response_json['message'] == 'success'

            perfil_deportivo: PerfilDeportivo = PerfilDeportivo.query.filter_by(id_deportista=deportista.id).first()

            db_session.delete(perfil_deportivo)
            db_session.commit()

    @patch('requests.post')
    def test_agregar_perfil_deportivo_con_datos_vacios(self, mock_post, setup_data):
        with app.test_client() as test_client:
            deportista: Deportista = setup_data['deportista']

            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                'token_valido': True, 'email': deportista.email}
            mock_post.return_value = mock_response


            body = {
                'id_deportista': deportista.id,
                "FTP_actual": "",
                "VO2max_actual": "",
                "detalle_lesion_molestia_incapacidad": "",
                "dias_semana_practica": "",
                "lesion_molestia_incapacidad": "",
                "tiempo_practica": "",
            }

            headers = {'Authorization': 'Bearer 123'}

            response = test_client.post(
                '/gestor-usuarios/perfil-deportivo/agregar', headers=headers, json=body, follow_redirects=True)
            response_json = json.loads(response.data)

            assert response.status_code == 400

    @patch('requests.post')
    def test_consultar_perfil_deportivo(self, mock_post, setup_data):
        with app.test_client() as test_client:
            deportista: Deportista = setup_data['deportista']

            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                'token_valido': True, 'email': deportista.email}
            mock_post.return_value = mock_response


            perfildeportivo = PerfilDeportivo(id_deportista=deportista.id,
                FTP_actual=fake.random_int(min=50, max=100),
                VO2max_actual= fake.random_int(min=50, max=100),
                detalle_lesion_molestia_incapacidad=fake.text(),
                dias_semana_practica=fake.random_int(min=1, max=7),
                lesion_molestia_incapacidad=True,
                tiempo_practica=fake.random_int(min=50, max=100))
            db_session.add(perfildeportivo)
            db_session.commit()

            headers = {'Authorization': 'Bearer 123'}

            response = test_client.get(
                '/gestor-usuarios/perfil-deportivo/consultar', headers=headers, follow_redirects=True)
            response_json = json.loads(response.data)

            assert response.status_code == 200
            #assert response_json['message'] == 'success'

            db_session.delete(perfildeportivo)
            db_session.commit()

    @patch('requests.post')
    def test_actualizar_perfil_deportivo(self, mock_post, setup_data):
        with app.test_client() as test_client:
            deportista: Deportista = setup_data['deportista']

            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                'token_valido': True, 'email': deportista.email}
            mock_post.return_value = mock_response


            perfildeportivo = PerfilDeportivo(id_deportista=deportista.id,
                FTP_actual=fake.random_int(min=50, max=100),
                VO2max_actual= fake.random_int(min=50, max=100),
                detalle_lesion_molestia_incapacidad=fake.text(),
                dias_semana_practica=fake.random_int(min=1, max=7),
                lesion_molestia_incapacidad=True,
                tiempo_practica=fake.random_int(min=50, max=100))
            db_session.add(perfildeportivo)
            db_session.commit()

            headers = {'Authorization': 'Bearer 123'}

            body = {
                'FTP_actual': fake.random_int(min=50, max=100),
                'VO2max_actual': fake.random_int(min=50, max=100),
                'detalle_lesion_molestia_incapacidad': fake.text(),
                'dias_semana_practica': fake.random_int(min=1, max=7),
                'lesion_molestia_incapacidad': True,
                'tiempo_practica': fake.random_int(min=50, max=100)
            }

            response = test_client.put(
                '/gestor-usuarios/perfil-deportivo/actualizar', headers=headers, json=body, follow_redirects=True)
            response_json = json.loads(response.data)

            assert response.status_code == 200
            assert response_json['message'] == 'success'

            db_session.delete(perfildeportivo)
            db_session.commit()
