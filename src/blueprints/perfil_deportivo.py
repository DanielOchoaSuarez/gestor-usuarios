import logging

from flask import Blueprint, jsonify, make_response, request
from src.commands.perfil.agregar_perfil_deportivo import AgregarPerfilDeportivo
from src.commands.perfil.buscar_perfil_deportivo import BuscarPerfilDeportivo
from src.commands.perfil.actualizar_perfil_deportivo import ActualizarPerfilDeportivo
from src.utils.seguridad_utils import UsuarioToken, token_required


logger = logging.getLogger(__name__)
perfil_deportivo_blueprint = Blueprint('perfil-deportivo', __name__)


@perfil_deportivo_blueprint.route('/agregar', methods=['POST'])
@token_required
def agregar_perfil_deportivo(usuario_token: UsuarioToken):
    logger.info(f'Agregando perfil deportivo a {usuario_token.email}')
    body = request.get_json()

    info = {
        'email': usuario_token.email,
        'dias_semana_practica': body.get('dias_semana_practica', None),
        'tiempo_practica': body.get('tiempo_practica', None),
        'VO2max_actual': body.get('VO2max_actual', None),
        'FTP_actual': body.get('FTP_actual', None),
        'lesion_molestia_incapacidad': body.get('lesion_molestia_incapacidad', None),
        'detalle_lesion_molestia_incapacidad': body.get('detalle_lesion_molestia_incapacidad', None)
    }

    result = AgregarPerfilDeportivo(usuario_token, info).execute()
    return make_response(jsonify(result), 200)


@perfil_deportivo_blueprint.route('/consultar', methods=['GET'])
@token_required
def buscar_perfil_deportivo(usuario_token: UsuarioToken):
    logger.info(f'Buscando perfil deportivo a {usuario_token.email}')

    info = {
        'email': usuario_token.email
    }

    result = BuscarPerfilDeportivo(usuario_token, info).execute()
    return make_response(jsonify(result), 200)


@perfil_deportivo_blueprint.route('/actualizar', methods=['PUT'])
@token_required
def actualizar_perfil_deportivo(usuario_token: UsuarioToken):
    logger.info(f'Actualzar perfil deportivo a {usuario_token.email}')

    body = request.get_json()

    info = {
        'email': usuario_token.email,
        'dias_semana_practica': body.get('dias_semana_practica', None),
        'tiempo_practica': body.get('tiempo_practica', None),
        'VO2max_actual': body.get('VO2max_actual', None),
        'FTP_actual': body.get('FTP_actual', None),
        'lesion_molestia_incapacidad': body.get('lesion_molestia_incapacidad', None),
        'detalle_lesion_molestia_incapacidad': body.get('detalle_lesion_molestia_incapacidad', None)
    }

    result = ActualizarPerfilDeportivo(usuario_token, info).execute()
    return make_response(jsonify(result), 200)