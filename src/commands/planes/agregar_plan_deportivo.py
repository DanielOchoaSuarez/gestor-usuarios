import datetime
import logging

from dateutil import parser
from src.commands.base_command import BaseCommand
from src.errors.errors import BadRequest, ErrorAgendandoSesion
from src.models.db import db_session
from src.models.deportista import Deportista
from src.models.plan_deportista import PlanDeportista
from src.utils.seguridad_utils import UsuarioToken
from src.utils.sesiones import agendar_sesion
from src.utils.str_utils import str_none_or_empty


logger = logging.getLogger(__name__)


class AgregarPlanDeportivo(BaseCommand):
    def __init__(self, usuario_token: UsuarioToken, info: dict):
        logger.info(
            'Agregar plan deportivo a usuario deportista')

        self.usuario_token: UsuarioToken = usuario_token

        if str_none_or_empty(info.get('email')):
            logger.error("email no puede ser vacio o nulo")
            raise BadRequest

        if str_none_or_empty(info.get('id_plan')):
            logger.error("El plan no puede ser vacio o nulo")
            raise BadRequest

        if str_none_or_empty(info.get('fecha_sesion')):
            logger.error("La fecha de sesion no puede ser vacia o nula")
            raise BadRequest

        fecha_sesion = parser.parse(info.get('fecha_sesion'))
        fecha_sistema = datetime.datetime.now()
        if fecha_sesion.date() < fecha_sistema.date():
            logger.error(
                "La fecha de sesion no puede ser menor a la fecha actual")
            raise BadRequest

        self.email = info.get('email')
        self.id_plan = info.get('id_plan')
        self.fecha_sesion = fecha_sesion

    def execute(self):
        deportista: Deportista = Deportista.query.filter_by(
            email=self.email).first()

        planes = PlanDeportista.query.filter_by(
            id_plan=self.id_plan,
            id_deportista=deportista.id).all()

        plan_deportista: PlanDeportista
        if len(planes) > 0:
            logger.info(
                f"El plan {self.id_plan} ya fue asignado al deportista {deportista.id}")
            plan_deportista = planes[0]
        else:
            logger.info(
                f"El plan {self.id_plan} no ha sido asignado al deportista {deportista.id}")

            plan = {
                'id_plan': self.id_plan,
                'id_deportista': deportista.id
            }

            plan_deportista = PlanDeportista(**plan)
            db_session.add(plan_deportista)
            db_session.commit()
            logger.info(f'Plan deportivo creado {plan_deportista.id}')

        sesion = agendar_sesion(self.usuario_token,
                                str(plan_deportista.id), str(self.fecha_sesion))

        if sesion is None:
            logger.error(
                f"Error agendando sesion para plan deportista {plan_deportista.id}")
            raise ErrorAgendandoSesion

        resp = {
            'id_plan_deportista': plan_deportista.id,
            'sesion': sesion
        }

        return resp
