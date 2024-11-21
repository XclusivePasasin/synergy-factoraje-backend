from flask import Blueprint, request
from services.usuario_service import UsuarioService
from utils.response import response_success, response_error

usuarios_bp = Blueprint('usuario', __name__)

@usuarios_bp.route('/crear-usuario', methods=['POST'])
def crear_usuario():
    data = request.get_json()
    if not data:
        return response_error("Datos no proporcionados", http_status=400)

    # Llamar al servicio para crear el usuario
    try:
        return UsuarioService.create_user(data)
    except Exception as e:
        return response_error(f"Error interno: {str(e)}", http_status=500)
