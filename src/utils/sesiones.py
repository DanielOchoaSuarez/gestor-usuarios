import os
import logging
import requests

from src.errors.errors import SesionYaAgendada


logger = logging.getLogger(__name__)


URL_GESTOR_SESIONES = os.getenv(
    'URL_GESTOR_SESIONES', 'http://127.0.0.1:3005')

URL_REGISTRAR_SESION = URL_GESTOR_SESIONES + \
    '/gestor-sesion-deportiva/sesiones/agendar_sesion'


def agendar_sesion(id_plan_deportista: str, fecha_sesion: str):
    logger.info(
        f'Agendando sesion plan deportista {id_plan_deportista} en fecha {fecha_sesion}')
    try:
        body = {
            'id_plan_deportista': id_plan_deportista,
            'fecha_sesion': fecha_sesion
        }
        response = requests.post(
            url=URL_REGISTRAR_SESION, json=body)

        if response.status_code == 200:
            data = response.json()
            return data['result']
        else:
            logger.error('1 Error agendando sesion plan deportista')
            logger.error(response.status_code)
            logger.error(response.text)
            if response.status_code == 400 and 'sesion_ya_agendada' in response.text:
                raise SesionYaAgendada

            return None

    except SesionYaAgendada:
        raise SesionYaAgendada

    except Exception as e:
        logger.error('2 Error agendando sesion plan deportista' + str(e))
        return None
