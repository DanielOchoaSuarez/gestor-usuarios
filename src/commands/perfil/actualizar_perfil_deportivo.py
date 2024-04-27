import logging

from src.commands.base_command import BaseCommand
from src.errors.errors import BadRequest
from src.models.db import db_session
from src.models.deportista import Deportista
from src.models.perfil_deportivo import PerfilDeportivo
from src.utils.seguridad_utils import UsuarioToken
from src.utils.str_utils import str_none_or_empty


logger = logging.getLogger(__name__)


class ActualizarPerfilDeportivo(BaseCommand):
    def __init__(self, usuario_token: UsuarioToken, info: dict):
        logger.info(
            'Actualizar perfil alimenticio a usuario deportista')

        super().__init__()
        self.__dict__.update(info)
        self.info = info

        self.usuario_token: UsuarioToken = usuario_token
        
        if str_none_or_empty(info.get('email')):
            logger.error("email no puede ser vacio o nulo")
            raise BadRequest


    def execute(self):
        deportista: Deportista = Deportista.query.filter_by(email=self.usuario_token.email).first()

        if deportista is None:
            logger.error("Deportista No Existe")
            raise BadRequest
        else:

            logger.info(f"Actualizando Perfil Deportivo: {deportista.email}")

            perfil_deportivo: PerfilDeportivo = PerfilDeportivo.query.filter_by(id_deportista=deportista.id).first()
            if perfil_deportivo is None:
                logger.error("Perfil Deportivo No Existe")
                raise BadRequest
            else:
                perfil_deportivo.dias_semana_practica = self.dias_semana_practica
                perfil_deportivo.tiempo_practica = self.tiempo_practica
                perfil_deportivo.VO2max_actual = self.VO2max_actual
                perfil_deportivo.FTP_actual = self.FTP_actual                
                perfil_deportivo.lesion_molestia_incapacidad = self.lesion_molestia_incapacidad
                perfil_deportivo.detalle_lesion_molestia_incapacidad = self.detalle_lesion_molestia_incapacidad

            db_session.commit()
            response = {
                'message': 'success'
            }

        return response
