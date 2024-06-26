import json
import uuid
import pytest
import logging
from unittest.mock import patch, MagicMock

from faker import Faker
from src.main import app
from src.models.db import db_session
from src.models.deportista import Deportista
from src.models.perfil_alimenticio_deportista import PerfilAlimenticioDeportista


fake = Faker()
logger = logging.getLogger(__name__)


@pytest.fixture(scope="class")
def setup_data():
    logger.info("Inicio Test Perfil Alimenticio")

    with db_session() as session:

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

        yield {
            'id_deportista': deportista_random.id,
            'email_deportista': deportista_random.email,
        }

        logger.info("Fin Test Perfil Alimenticio")
        session.delete(deportista_random)
        session.commit()


@pytest.mark.usefixtures("setup_data")
class TestPerfilAlimenticio():

    @patch('requests.post')
    def test_agregar_perfil_alimenticio(self, mock_post, setup_data):

        with db_session() as session:
            with app.test_client() as test_client:
                id_deportista: Deportista = setup_data['id_deportista']
                email_deportista: Deportista = setup_data['email_deportista']

                mock_response = MagicMock()
                mock_response.status_code = 200
                mock_response.json.return_value = {
                    'token_valido': True, 'email': email_deportista}
                mock_post.return_value = mock_response

                body = {
                    'id_deportista': id_deportista,
                    "intorelancia_alergia": True,
                    "detalle_intolerancia_alergia": fake.text(),
                    "vegano": True,
                    "objetivo_peso": fake.random_int(min=50, max=100)
                }

                headers = {'Authorization': 'Bearer 123'}

                response = test_client.post(
                    '/gestor-usuarios/perfil-alimenticio/agregar', headers=headers, json=body, follow_redirects=True)
                response_json = json.loads(response.data)

                assert response.status_code == 200
                assert response_json['message'] == 'success'

                perfil_alimenticio: PerfilAlimenticioDeportista = session.query(PerfilAlimenticioDeportista).filter(
                    PerfilAlimenticioDeportista.id_deportista == id_deportista).first()

                session.delete(perfil_alimenticio)
                session.commit()

    @patch('requests.post')
    def test_agregar_perfil_alimencio_con_datos_vacios(self, mock_post, setup_data):
        with app.test_client() as test_client:
            id_deportista: Deportista = setup_data['id_deportista']
            email_deportista: Deportista = setup_data['email_deportista']

            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                'token_valido': True, 'email': email_deportista}
            mock_post.return_value = mock_response

            body = {
                'id_deportista': id_deportista,
                "intorelancia_alergia": "",
                "detalle_intolerancia_alergia": "",
                "vegano": "",
                "objetivo_peso": ""
            }

            headers = {'Authorization': 'Bearer 123'}

            response = test_client.post(
                '/gestor-usuarios/perfil-alimenticio/agregar', headers=headers, json=body, follow_redirects=True)
            response_json = json.loads(response.data)

            assert response.status_code == 400

    @patch('requests.post')
    def test_consultar_perfil_alimenticio(self, mock_post, setup_data):
        with db_session() as session:
            with app.test_client() as test_client:
                id_deportista: Deportista = setup_data['id_deportista']
                email_deportista: Deportista = setup_data['email_deportista']

                mock_response = MagicMock()
                mock_response.status_code = 200
                mock_response.json.return_value = {
                    'token_valido': True, 'email': email_deportista}
                mock_post.return_value = mock_response

                perfilalimenticio = PerfilAlimenticioDeportista(id_deportista=id_deportista,
                                                                intorelancia_alergia=True,
                                                                detalle_intolerancia_alergia=fake.text(),
                                                                vegano=True,
                                                                objetivo_peso=fake.random_int(min=50, max=100))
                session.add(perfilalimenticio)
                session.commit()

                headers = {'Authorization': 'Bearer 123'}

                response = test_client.get(
                    '/gestor-usuarios/perfil-alimenticio/consultar', headers=headers, follow_redirects=True)
                response_json = json.loads(response.data)

                assert response.status_code == 200

                session.delete(perfilalimenticio)
                session.commit()

    @patch('requests.post')
    def test_actualizar_perfil_alimenticio(self, mock_post, setup_data):
        with db_session() as session:
            with app.test_client() as test_client:
                id_deportista: Deportista = setup_data['id_deportista']
                email_deportista: Deportista = setup_data['email_deportista']

                mock_response = MagicMock()
                mock_response.status_code = 200
                mock_response.json.return_value = {
                    'token_valido': True, 'email': email_deportista}
                mock_post.return_value = mock_response

                perfilalimenticio = PerfilAlimenticioDeportista(id_deportista=id_deportista,
                                                                intorelancia_alergia=True,
                                                                detalle_intolerancia_alergia=fake.text(),
                                                                vegano=True,
                                                                objetivo_peso=fake.random_int(min=50, max=100))
                session.add(perfilalimenticio)
                session.commit()

                headers = {'Authorization': 'Bearer 123'}

                body = {
                    'id_deportista': id_deportista,
                    "intorelancia_alergia": False,
                    "detalle_intolerancia_alergia": fake.text(),
                    "vegano": False,
                    "objetivo_peso": fake.random_int(min=50, max=100)
                }

                response = test_client.put(
                    '/gestor-usuarios/perfil-alimenticio/actualizar', headers=headers, json=body, follow_redirects=True)
                response_json = json.loads(response.data)

                assert response.status_code == 200
                assert response_json['message'] == 'success'

                session.delete(perfilalimenticio)
                session.commit()
