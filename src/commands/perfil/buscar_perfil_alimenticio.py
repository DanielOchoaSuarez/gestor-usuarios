import datetime
import logging

from dateutil import parser
from src.commands.base_command import BaseCommand
from src.errors.errors import BadRequest, ErrorAgendandoSesion
from src.models.db import db_session
from src.models.deportista import Deportista
from src.models.perfil_alimenticio_deportista import PerfilAlimenticioDeportista, PerfilAlimenticioDeportistaSchema
from src.utils.seguridad_utils import UsuarioToken
from src.utils.str_utils import str_none_or_empty


logger = logging.getLogger(__name__)


class BuscarPerfilAlimenticio(BaseCommand):
    def __init__(self, usuario_token: UsuarioToken, info: dict):
        logger.info(
            'Buscar perfil alimenticio a usuario deportista')

        self.usuario_token: UsuarioToken = usuario_token
        self.info = info

        if str_none_or_empty(info.get('email')):
            logger.error("email no puede ser vacio o nulo")
            raise BadRequest


    def execute(self):
        deportista: Deportista = Deportista.query.filter_by(email=self.usuario_token.email).first()

        if deportista is None:
            logger.error("Deportista No Existe")
            raise BadRequest
        else:
            logger.info(f"Buscando Perfil Alimenticio: {deportista.email}")
            perfil_alimenticio: PerfilAlimenticioDeportista = PerfilAlimenticioDeportista.query.filter_by(id_deportista=deportista.id).first()

            if perfil_alimenticio is None:
                logger.error("Perfil Alimenticio No Existe")
                raise BadRequest
            else:
                schema = PerfilAlimenticioDeportistaSchema()
                return schema.dump(perfil_alimenticio)
