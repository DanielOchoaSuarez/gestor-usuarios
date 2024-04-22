import logging

from flask import Blueprint, jsonify, make_response, request
from src.commands.planes.agregar_plan_deportivo import AgregarPlanDeportivo
from src.commands.planes.obtener_planes_deportivos import ObtenerPlanesDeportivos
from src.commands.planes.obtener_planes_deportista import ObtenerPlanesDeportista
from src.utils.seguridad_utils import UsuarioToken, token_required


logger = logging.getLogger(__name__)
planes_blueprint = Blueprint('planes', __name__)


@planes_blueprint.route('/obtener_planes_deportista', methods=['GET'])
@token_required
def obtener_planes_deportista(usuario_token: UsuarioToken):
    logger.info(f'Obteniendo planes del deportista {usuario_token.email}')
    info = {
        'email': usuario_token.email,
    }
    result = ObtenerPlanesDeportista(**info).execute()
    return make_response(jsonify(result), 200)


@planes_blueprint.route('/obtener_planes_deportivos', methods=['GET'])
def obtener_planes():
    logger.info('Obteniendo todos los planes deportivos')
    result = ObtenerPlanesDeportivos().execute()
    return make_response(jsonify(result), 200)


@planes_blueprint.route('/agregar_plan_deportivo', methods=['POST'])
@token_required
def agregar_plan_deportivo(usuario_token: UsuarioToken):
    logger.info(f'Agregando plan deportivo a {usuario_token.email}')
    body = request.get_json()

    info = {
        'email': usuario_token.email,
        'id_plan': body.get('id_plan', None),
        'fecha_sesion': body.get('fecha_sesion', None),
    }

    result = AgregarPlanDeportivo(info).execute()
    return make_response(jsonify(result), 200)
