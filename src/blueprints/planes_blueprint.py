import logging

from flask import Blueprint, jsonify, make_response
from src.commands.planes.obtener_planes_deportivos import ObtenerPlanesDeportivos
from src.commands.planes.obtener_planes_deportista import ObtenerPlanesDeportista
from src.utils.seguridad_utils import UsuarioToken, token_required


logger = logging.getLogger(__name__)
planes_blueprint = Blueprint('planes', __name__)


@planes_blueprint.route('/obtener_planes_deportista', methods=['GET'])
@token_required
def obtener_planes_deportista(deportista_token: UsuarioToken):
    logger.info(f'Obteniendo planes del deportista {deportista_token.email}')
    info = {
        'email': deportista_token.email,
    }
    result = ObtenerPlanesDeportista(**info).execute()
    return make_response(jsonify(result), 200)


@planes_blueprint.route('/obtener_planes_deportivos', methods=['GET'])
def obtener_planes():
    logger.info('Obteniendo todos los planes deportivos')
    result = ObtenerPlanesDeportivos().execute()
    return make_response(jsonify(result), 200)
