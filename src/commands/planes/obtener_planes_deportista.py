import logging

from src.commands.base_command import BaseCommand
from src.errors.errors import BadRequest
from src.models.deportista import Deportista
from src.models.plan import Plan
from src.models.plan_deportista import PlanDeportista
from src.utils.alimentacion import obtener_plan_alimenticio
from src.utils.deportes import obtener_plan_deportivo
from src.utils.str_utils import str_none_or_empty


logger = logging.getLogger(__name__)


class ObtenerPlanesDeportista(BaseCommand):
    def __init__(self, **info):
        logger.info(
            'Validando informacion para obtener planes del deportista')

        if str_none_or_empty(info.get('email')):
            logger.error("email no puede ser vacio o nulo")
            raise BadRequest

        self.email = info.get('email')

    def execute(self):
        deportista: Deportista = Deportista.query.filter_by(
            email=self.email).first()
        logger.info(f'Obteniendo planes del deportista {deportista.id}')

        planes = PlanDeportista.query.filter_by(
            id_deportista=deportista.id).all()

        if planes is None or len(planes) == 0:
            logger.error("Plan de alimentacion no encontrado")
            return []

        respuesta = []

        plan: PlanDeportista
        for plan in planes:
            id_plan = str(plan.id_plan)

            ejercicios = []
            tmp_deportes = obtener_plan_deportivo(id_plan)
            if tmp_deportes is not None:
                for p in tmp_deportes['result']:
                    ejercicios.append(p)

            alimentos = []
            tmp_alimentos = obtener_plan_alimenticio(id_plan)
            if tmp_alimentos is not None:
                for p in tmp_alimentos['result']:
                    alimentos.append(p)

            resp_tmp = {
                'nombre_plan': plan.plan.nombre,
                'vo2': plan.plan.vo2,
                'descripcion': plan.plan.descripcion,
                'ejercicios': ejercicios,
                'alimentos': alimentos,
            }
            respuesta.append(resp_tmp)

        return respuesta
