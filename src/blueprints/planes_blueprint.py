import os
import logging
from flask import Blueprint, jsonify, make_response, request
from src.commands.planes.obtener_plan import ObtenerPlanes


logger = logging.getLogger(__name__)
planes_blueprint = Blueprint('planes', __name__)


@planes_blueprint.route('/obtener_planes_deportista', methods=['POST'])
def obtener_planes():
    body = request.get_json()
    info = {
        'id_deportista': body.get('id_deportista', None),
    }
    result = ObtenerPlanes(**info).execute()
    return make_response(jsonify(result), 200)
