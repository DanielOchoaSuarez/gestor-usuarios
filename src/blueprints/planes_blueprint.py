import logging

from flask import Blueprint, jsonify, make_response, request
from src.commands.planes.agregar_plan_deportivo import AgregarPlanDeportivo
from src.commands.planes.obtener_alimentos_plan_deportista import ObtenerAlimentosPlanDeportista
from src.commands.planes.obtener_ejercicios_plan_deportista import ObtenerEjerciciosPlanDeportista
from src.commands.planes.obtener_planes_deportivos import ObtenerPlanesDeportivos
from src.commands.planes.obtener_planes_deportista import ObtenerPlanesDeportista
from src.commands.planes.obtener_sugerencia_alimentos import ObtenerSugerenciaAlimentos
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

    result = AgregarPlanDeportivo(usuario_token, info).execute()
    return make_response(jsonify(result), 200)


@planes_blueprint.route('/obtener_ejercicios_plan_deportista/<id_plan_deportista>/<id_sesion>', methods=['GET'])
@token_required
def obtener_ejercicios_plan_deportist(usuario_token: UsuarioToken, id_plan_deportista: str, id_sesion: str):
    logger.info('Obteniendo todos los ejercicios deportivos')
    info = {
        'email': usuario_token.email,
        'id_plan_deportista': id_plan_deportista,
        'id_sesion': id_sesion,
    }
    result = ObtenerEjerciciosPlanDeportista(**info).execute()
    return make_response(jsonify(result), 200)


@planes_blueprint.route('/obtener_alimentos_plan/<id_plan_deportista>', methods=['GET'])
def obtener_alimentos_plan(id_plan_deportista: str = None):
    logger.info('Obteniendo alimentos por id plan deportista')
    info = {
        'id_plan_deportista': id_plan_deportista,
    }
    result = ObtenerAlimentosPlanDeportista(**info).execute()
    return make_response(jsonify(result), 200)


@planes_blueprint.route('/obtener_sugerencia_alimentos/<id_plan>', methods=['GET'])
def obtener_sugerencia_alimentos(id_plan: str = None):
    logger.info('Obteniendo sugerencias alimentos por id plan')
    info = {
        'id_plan': id_plan,
    }
    result = ObtenerSugerenciaAlimentos(**info).execute()
    return make_response(jsonify(result), 200)
