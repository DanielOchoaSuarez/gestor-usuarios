import datetime
import logging

from src.commands.base_command import BaseCommand
from src.errors.errors import BadRequest
from src.models.db import db_session
from src.models.deportista import Deportista
from src.models.perfil_alimenticio_deportista import PerfilAlimenticioDeportista
from src.utils.seguridad_utils import UsuarioToken
from src.utils.str_utils import str_none_or_empty


logger = logging.getLogger(__name__)


class ActualizarPerfilAlimenticio(BaseCommand):
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
        with db_session() as session:

            deportista: Deportista = session.query(Deportista).filter(
                Deportista.email == self.usuario_token.email).first()

            if deportista is None:
                logger.error("Deportista No Existe")
                raise BadRequest
            else:

                logger.info(
                    f"Actualizando Perfil Alimenticio: {deportista.email}")

                perfil_alimenticio: PerfilAlimenticioDeportista = session.query(PerfilAlimenticioDeportista).filter(
                    PerfilAlimenticioDeportista.id_deportista == deportista.id).first()

                if perfil_alimenticio is None:
                    logger.error("Perfil Alimenticio No Existe")
                    raise BadRequest
                else:
                    perfil_alimenticio.intorelancia_alergia = self.intorelancia_alergia
                    perfil_alimenticio.detalle_intolerancia_alergia = self.detalle_intolerancia_alergia
                    perfil_alimenticio.vegano = self.vegano
                    perfil_alimenticio.objetivo_peso = self.objetivo_peso

                session.commit()
                response = {
                    'message': 'success'
                }

            return response
