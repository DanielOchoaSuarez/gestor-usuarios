import logging

from src.commands.base_command import BaseCommand
from src.errors.errors import BadRequest
from src.models.db import db_session
from src.models.deportista import Deportista
from src.models.perfil_deportivo import PerfilDeportivo
from src.utils.seguridad_utils import UsuarioToken
from src.utils.str_utils import str_none_or_empty


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
        deportista: Deportista = Deportista.query.filter_by(email=self.usuario_token.email).first()

        if self.info.get('dias_semana_practica') == "" or self.info.get('tiempo_practica') == "" or self.info.get('VO2max_actual') == "" or self.info.get('FTP_actual') == "" or self.info.get('lesion_molestia_incapacidad') == "" or self.info.get('detalle_lesion_molestia_incapacidad') == "":
            logger.error("Información invalida")
            raise BadRequest

        # Validar que la información no sea vacía
        if deportista is None:
            logger.error("Deportista No Existe")
            raise BadRequest
        else:
            logger.info(f"Registrando Perfil Deportivo: {deportista.email}")

            record = PerfilDeportivo(id_deportista=deportista.id,
                                                 dias_semana_practica=self.info.get('dias_semana_practica'),
                                                 tiempo_practica=self.info.get('tiempo_practica'),
                                                 VO2max_actual=self.info.get('VO2max_actual'),
                                                 FTP_actual=self.info.get('FTP_actual'),
                                                 lesion_molestia_incapacidad=self.info.get('lesion_molestia_incapacidad'),
                                                 detalle_lesion_molestia_incapacidad=self.info.get('detalle_lesion_molestia_incapacidad'))


            db_session.add(record)
            db_session.commit()
            response = {
                'message': 'success'
            }

        return response
