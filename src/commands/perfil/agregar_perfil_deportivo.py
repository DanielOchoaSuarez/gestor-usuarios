import logging

from src.commands.base_command import BaseCommand
from src.errors.errors import BadRequest
from src.models.db import db_session
from src.models.deportista import Deportista
from src.models.perfil_deportivo import PerfilDeportivo
from src.models.plan import Plan
from src.models.plan_deportista import PlanDeportista
from src.utils.seguridad_utils import UsuarioToken
from src.utils.str_utils import str_none_or_empty
from faker import Faker


logger = logging.getLogger(__name__)


class AgregarPerfilDeportivo(BaseCommand):
    def __init__(self, usuario_token: UsuarioToken, info: dict):
        logger.info(
            'Agregar perfil deportivo a usuario deportista')

        self.usuario_token: UsuarioToken = usuario_token
        self.info = info

        if str_none_or_empty(info.get('email')):
            logger.error("email no puede ser vacio o nulo")
            raise BadRequest

    def execute(self):

        with db_session() as session:

            deportista: Deportista = session.query(Deportista).filter(
                Deportista.email == self.usuario_token.email).first()

            if self.info.get('dias_semana_practica') == "" or self.info.get('tiempo_practica') == "" or self.info.get('VO2max_actual') == "" or self.info.get('FTP_actual') == "" or self.info.get('lesion_molestia_incapacidad') == "" or self.info.get('detalle_lesion_molestia_incapacidad') == "":
                logger.error("Información invalida")
                raise BadRequest

            # Validar que la información no sea vacía
            if deportista is None:
                logger.error("Deportista No Existe")
                raise BadRequest
            else:
                logger.info(
                    f"Registrando Perfil Deportivo: {deportista.email}")

                # Almacenando el perfil deportivo del usuario
                record = PerfilDeportivo(id_deportista=deportista.id,
                                         dias_semana_practica=self.info.get(
                                             'dias_semana_practica'),
                                         tiempo_practica=self.info.get(
                                             'tiempo_practica'),
                                         VO2max_actual=self.info.get(
                                             'VO2max_actual'),
                                         FTP_actual=self.info.get(
                                             'FTP_actual'),
                                         lesion_molestia_incapacidad=self.info.get(
                                             'lesion_molestia_incapacidad'),
                                         detalle_lesion_molestia_incapacidad=self.info.get('detalle_lesion_molestia_incapacidad'))
                session.add(record)
                session.commit()

                # Asignando un plan *deportivo y alimenticio al deportista
                plan_deportista_actual = session.query(PlanDeportista).filter(
                    PlanDeportista.id_deportista == deportista.id).first()

                if plan_deportista_actual is None:
                    plan_tmp: Plan = session.query(Plan).all()
                    lista_planes = len(plan_tmp)
                    if lista_planes == 0:
                        logger.error("No hay planes registrados")
                        raise BadRequest
                    else:
                        fake = Faker()
                        indica_plan_seleccionado = fake.random_int(
                            min=0, max=(lista_planes-1))
                        plan_seleccionado = plan_tmp[indica_plan_seleccionado]

                        record_plan_deportista = PlanDeportista(
                            id_deportista=deportista.id, id_plan=plan_seleccionado.id)
                        session.add(record_plan_deportista)
                        session.commit()

                response = {
                    'message': 'success'
                }

            return response
