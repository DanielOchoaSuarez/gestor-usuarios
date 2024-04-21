import os
import logging
import requests


logger = logging.getLogger(__name__)


URL_GESTOR_DEPORTES = os.getenv('URL_GESTOR_DEPORTES', 'http://127.0.0.1:3003')

URL_OBTENER_PLAN_DEPORTIVO = URL_GESTOR_DEPORTES + \
    '/gestor-deportes/deportes/obtener_plan'


def obtener_plan_deportivo(id_plan: str):
    logger.info(
        f'Obteniendo plan deportivo con id {id_plan}')
    try:
        response = requests.post(
            url=URL_OBTENER_PLAN_DEPORTIVO, json={"id_plan": id_plan})

        if response.status_code == 200:
            data = response.json()
            return data
        else:
            logger.error('Error obteniendo plan deportivo')
            return None

    except Exception as e:
        logger.error(f'Error obteniendo plan deportivo {e}')
        return None
