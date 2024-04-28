import logging


from src.commands.base_command import BaseCommand
from src.errors.errors import BadRequest
from src.models.deportista import Deportista
from src.models.plan import Plan
from src.models.plan_deportista import PlanDeportista
from src.utils.deportes import obtener_plan_deportivo
from src.utils.str_utils import str_none_or_empty


logger = logging.getLogger(__name__)


class ObtenerEjerciciosPlanDeportista(BaseCommand):
    def __init__(self, **info):

        if str_none_or_empty(info.get('email')):
            logger.error("email no puede ser vacio o nulo")
            raise BadRequest

        if str_none_or_empty(info.get('id_plan_deportista')):
            logger.error("id_plan_deportista no puede ser vacio o nulo")
            raise BadRequest

        self.email = info.get('email')
        self.id_plan_deportista = info.get('id_plan_deportista')

    def execute(self):
        logger.info(
            f'Obteniendo ejercicios plan deportista {self.id_plan_deportista}')

        deportista: Deportista = Deportista.query.filter_by(
            email=self.email).first()

        plan_deportista: PlanDeportista = PlanDeportista.query.filter_by(
            id=self.id_plan_deportista,
            id_deportista=deportista.id).first()

        if plan_deportista is None or plan_deportista.plan is None:
            logger.error(
                f'Plan deportista no encontrado. id {self.id_plan_deportista}, email {self.email}')
            return {}

        ejercicios = []
        tmp_deportes = obtener_plan_deportivo(str(plan_deportista.id_plan))
        if tmp_deportes is not None:
            for p in tmp_deportes['result']:
                ejercicios.append(p)

        plan: Plan = plan_deportista.plan
        resp_tmp = {
            'id_plan': plan.id,
            'nombre_plan': plan.nombre,
            'vo2': plan.vo2,
            'descripcion': plan.descripcion,
            'ejercicios': ejercicios,
        }

        return resp_tmp
