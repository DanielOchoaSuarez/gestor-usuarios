import logging


from src.commands.base_command import BaseCommand
from src.errors.errors import BadRequest
from src.models.db import db_session
from src.models.deportista import Deportista
from src.models.perfil_deportivo import PerfilDeportivo, PerfilDeportivoSchema
from src.utils.seguridad_utils import UsuarioToken
from src.utils.str_utils import str_none_or_empty


logger = logging.getLogger(__name__)


class BuscarPerfilDeportivo(BaseCommand):
    def __init__(self, usuario_token: UsuarioToken, info: dict):
        logger.info(
            'Buscar perfil deportivo a usuario deportista')

        self.usuario_token: UsuarioToken = usuario_token
        self.info = info

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
                logger.info(f"Buscando Perfil Deportivo: {deportista.email}")
                perfil_deportivo: PerfilDeportivo = PerfilDeportivo.query.filter_by(
                    id_deportista=deportista.id).first()

                if perfil_deportivo is None:
                    logger.error("Perfil Deportivo No Existe")
                    raise BadRequest
                else:
                    schema = PerfilDeportivoSchema()
                    return schema.dump(perfil_deportivo)
