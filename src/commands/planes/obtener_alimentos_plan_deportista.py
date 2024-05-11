import logging


from src.commands.base_command import BaseCommand
from src.errors.errors import BadRequest
from src.models.plan_deportista import PlanDeportista
from src.utils.alimentacion import obtener_plan_alimenticio
from src.utils.str_utils import str_none_or_empty


logger = logging.getLogger(__name__)


class ObtenerAlimentosPlanDeportista(BaseCommand):

    def __init__(self, **info):

        if str_none_or_empty(info.get('id_plan_deportista')):
            logger.error("id_plan_deportista no puede ser vacio o nulo")
            raise BadRequest

        self.id_plan_deportista = info.get('id_plan_deportista')

    def execute(self):
        logger.info(
            f'Obteniendo alimentos plan deportista {self.id_plan_deportista}')

        plan_deportista: PlanDeportista = PlanDeportista.query.filter_by(
            id=self.id_plan_deportista).first()

        if plan_deportista is None or plan_deportista.plan is None:
            logger.error(
                f'Plan deportista no encontrado. id {self.id_plan_deportista}')
            return {'alimentos': []}

        alimentos = []
        tmp_alimentos = obtener_plan_alimenticio(str(plan_deportista.id_plan))
        if tmp_alimentos is not None:
            for p in tmp_alimentos['result']:
                alimentos.append(p)

        resp_tmp = {
            'alimentos': alimentos,
        }

        return resp_tmp
