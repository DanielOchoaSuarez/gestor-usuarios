import logging

from flask import Blueprint, jsonify, make_response, request
from src.commands.perfil.agregar_perfil_alimenticio import AgregarPerfilAlimenticio
from src.commands.perfil.buscar_perfil_alimenticio import BuscarPerfilAlimenticio
from src.commands.perfil.actualizar_perfil_alimenticio import ActualizarPerfilAlimenticio
from src.utils.seguridad_utils import UsuarioToken, token_required


logger = logging.getLogger(__name__)
perfil_alimenticio_blueprint = Blueprint('perfil-alimenticio', __name__)


@perfil_alimenticio_blueprint.route('/agregar', methods=['POST'])
@token_required
def agregar_perfil_alimenticio(usuario_token: UsuarioToken):
    logger.info(f'Agregando perfil alimenticio a {usuario_token.email}')
    body = request.get_json()

    info = {
        'email': usuario_token.email,
        'intorelancia_alergia': body.get('intorelancia_alergia', None),
        'detalle_intolerancia_alergia': body.get('detalle_intolerancia_alergia', None),
        'vegano': body.get('vegano', None),
        'objetivo_peso': body.get('objetivo_peso', None)
    }

    result = AgregarPerfilAlimenticio(usuario_token, info).execute()
    return make_response(jsonify(result), 200)


@perfil_alimenticio_blueprint.route('/consultar', methods=['GET'])
@token_required
def buscar_perfil_alimenticio(usuario_token: UsuarioToken):
    logger.info(f'Buscando perfil alimenticio a {usuario_token.email}')

    info = {
        'email': usuario_token.email
    }

    result = BuscarPerfilAlimenticio(usuario_token, info).execute()
    return make_response(jsonify(result), 200)


@perfil_alimenticio_blueprint.route('/actualizar', methods=['PUT'])
@token_required
def actualizar_perfil_alimenticio(usuario_token: UsuarioToken):
    logger.info(f'Actualzar perfil alimenticio a {usuario_token.email}')

    body = request.get_json()

    info = {
        'email': usuario_token.email,
        'intorelancia_alergia': body.get('intorelancia_alergia', None),
        'detalle_intolerancia_alergia': body.get('detalle_intolerancia_alergia', None),
        'vegano': body.get('vegano', None),
        'objetivo_peso': body.get('objetivo_peso', None)
    }

    result = ActualizarPerfilAlimenticio(usuario_token, info).execute()
    return make_response(jsonify(result), 200)