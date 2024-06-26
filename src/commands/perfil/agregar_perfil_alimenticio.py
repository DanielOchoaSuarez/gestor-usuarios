import logging


from src.commands.base_command import BaseCommand
from src.errors.errors import BadRequest
from src.models.db import db_session
from src.models.deportista import Deportista
from src.models.perfil_alimenticio_deportista import PerfilAlimenticioDeportista
from src.utils.seguridad_utils import UsuarioToken
from src.utils.str_utils import str_none_or_empty


logger = logging.getLogger(__name__)


class AgregarPerfilAlimenticio(BaseCommand):
    def __init__(self, usuario_token: UsuarioToken, info: dict):
        logger.info(
            'Agregar perfil alimenticio a usuario deportista')

        self.usuario_token: UsuarioToken = usuario_token
        self.info = info

        if str_none_or_empty(info.get('email')):
            logger.error("email no puede ser vacio o nulo")
            raise BadRequest

    def execute(self):

        with db_session() as session:

            deportista: Deportista = session.query(Deportista).filter(
                Deportista.email == self.usuario_token.email).first()

            if self.info.get('intorelancia_alergia') == "" or self.info.get('detalle_intolerancia_alergia') == "" or self.info.get('vegano') == "" or self.info.get('objetivo_peso') == "":
                logger.error("Información invalida")
                raise BadRequest

            if deportista is None:
                logger.error("Deportista No Existe")
                raise BadRequest
            else:
                logger.info(
                    f"Registrando Perfil Alimenticio: {deportista.email}")
                record = PerfilAlimenticioDeportista(id_deportista=deportista.id,
                                                     intorelancia_alergia=self.info.get(
                                                         'intorelancia_alergia'),
                                                     detalle_intolerancia_alergia=self.info.get(
                                                         'detalle_intolerancia_alergia'),
                                                     vegano=self.info.get(
                                                         'vegano'),
                                                     objetivo_peso=self.info.get('objetivo_peso'))

                session.add(record)
                session.commit()
                response = {
                    'message': 'success'
                }

            return response
