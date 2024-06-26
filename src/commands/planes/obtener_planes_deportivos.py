import logging

from src.commands.base_command import BaseCommand
from src.models.db import db_session
from src.models.plan import Plan
from src.utils.deportes import obtener_plan_deportivo


logger = logging.getLogger(__name__)


class ObtenerPlanesDeportivos(BaseCommand):
    def __init__(self):
        '''
        Constructor para el comando ObtenerPlanesDeportivos
        '''

    def execute(self):
        logger.info('Obteniendo todos los planes deportivos')

        with db_session() as session:
            planes_bd = session.query(Plan).all()

            if planes_bd is None or len(planes_bd) == 0:
                logger.error("No existen planes deportivos configurados")
                return []

            respuesta = []

            plan: Plan
            for plan in planes_bd:
                tmp = obtener_plan_deportivo(str(plan.id))

                ejercicios = []
                for p in tmp['result']:
                    ejercicios.append(p)

                resp_tmp = {
                    'id_plan': plan.id,
                    'nombre_plan': plan.nombre,
                    'vo2': plan.vo2,
                    'descripcion': plan.descripcion,
                    'ejercicios': ejercicios,
                }
                respuesta.append(resp_tmp)

            return respuesta
