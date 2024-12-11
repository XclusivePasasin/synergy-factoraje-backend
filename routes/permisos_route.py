from flask import Blueprint, request
from models.permisos import Permiso
from models.menus import Menu
from models.roles import Rol
from utils.response import response_success, response_error
from utils.interceptor import token_required
from services.permisos_service import PermisosService

permisos_bp = Blueprint('permiso', __name__)

# endpoint for actualizar permisos
@permisos_bp.route('/actualizar-permisos', methods=['PUT'])
@token_required
def actualizar_permisos():
    try:
        data = request.get_json()
        if not data:
            return response_error("Datos no proporcionados", http_status=400)
        return PermisosService.actualizar_permisos(data)
    except Exception as e:
        return response_error(f"Error interno del servidor: {str(e)}", http_status=500)