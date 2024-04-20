import logging

from src.commands.base_command import BaseCommand
from src.errors.errors import BadRequest
from src.models.plan import Plan
from src.models.plan_deportista import PlanDeportista
from src.utils.alimentacion import obtener_plan_alimenticio
from src.utils.deportes import obtener_plan_deportivo
from src.utils.str_utils import str_none_or_empty


logger = logging.getLogger(__name__)


class ObtenerPlanes(BaseCommand):
    def __init__(self, **info):
        logger.info(
            'Validando informacion para obtener planes del deportista')

        if str_none_or_empty(info.get('id_deportista')):
            logger.error("id_deportista no puede ser vacio o nulo")
            raise BadRequest

        self.id_deportista = info.get('id_deportista')

    def execute(self):
        logger.info("Buscando planes del deportista")
        planes = PlanDeportista.query.filter_by(
            id_deportista=self.id_deportista).all()

        if planes is None or len(planes) == 0:
            logger.error("Plan de alimentacion no encontrado")
            return []

        planes_deportivos = []
        planes_alimentacion = []

        plan: PlanDeportista
        for plan in planes:
            id_plan = str(plan.id_plan)

            tmp_deportes = obtener_plan_deportivo(id_plan)
            if tmp_deportes is not None:
                for p in tmp_deportes['result']:
                    planes_deportivos.append(p)

            tmp_alimentos = obtener_plan_alimenticio(id_plan)
            if tmp_alimentos is not None:
                for p in tmp_alimentos['result']:
                    planes_alimentacion.append(p)

        resp = {
            'planes_deportivos': planes_deportivos,
            'planes_alimentacion': planes_alimentacion,
        }

        return resp
