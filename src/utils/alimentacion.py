import os
import logging
import requests


logger = logging.getLogger(__name__)


URL_GESTOR_PLAN_ALIMENTICIO = os.getenv(
    'URL_GESTOR_PLAN_ALIMENTICIO', 'http://127.0.0.1:3004')

URL_OBTENER_PLAN_ALIMENTICIO = URL_GESTOR_PLAN_ALIMENTICIO + \
    '/gestor-plan-alimenticio/alimentacion/obtener_plan'


def obtener_plan_alimenticio(id_plan: str):
    logger.info(
        f'Obteniendo plan alimenticio con id {id_plan}')
    try:
        response = requests.post(
            url=URL_OBTENER_PLAN_ALIMENTICIO, json={"id_plan": id_plan})

        if response.status_code == 200:
            data = response.json()
            return data
        else:
            logger.error('1 Error obteniendo plan alimenticio')
            return None

    except Exception as e:
        logger.error('2 Error obteniendo plan alimenticio' + str(e))
        return None
