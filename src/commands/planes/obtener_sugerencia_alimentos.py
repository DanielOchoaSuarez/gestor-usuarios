import logging


from src.commands.base_command import BaseCommand
from src.models.db import db_session
from src.errors.errors import BadRequest
from src.models.plan_deportista import PlanDeportista
from src.utils.alimentacion import obtener_plan_alimenticio
from src.utils.str_utils import str_none_or_empty


logger = logging.getLogger(__name__)


class ObtenerSugerenciaAlimentos(BaseCommand):

    def __init__(self, **info):

        if str_none_or_empty(info.get('id_plan')):
            logger.error("id_plan no puede ser vacio o nulo")
            raise BadRequest

        self.id_plan = info.get('id_plan')

    def execute(self):
        logger.info(
            f'Obteniendo sugerencia alimentos plan {self.id_plan}')

        with db_session() as session:

            plan_deportista = session.query(PlanDeportista).filter(
                PlanDeportista.id_plan == self.id_plan).first()

            if plan_deportista is None or plan_deportista.plan is None:
                logger.error(
                    f'Plan deportista no encontrado. id {self.id_plan}')
                return {'alimentos': []}

            alimentos = []
            tmp_alimentos = obtener_plan_alimenticio(
                str(plan_deportista.id))
            if tmp_alimentos is not None:
                for p in tmp_alimentos['result']:
                    alimentos.append(p)

            resp_tmp = {
                'alimentos': alimentos,
            }

            return resp_tmp
