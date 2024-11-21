from flask import Blueprint, request
from services.usuario_service import UsuarioService
from utils.response import response_success, response_error

usuarios_bp = Blueprint('usuario', __name__)

@usuarios_bp.route('/crear-usuario', methods=['POST'])  
def crear_usuario():
    """
    Endpoint para crear un usuario.
    """
    try:
        data = request.get_json()
        if not data:
            return response_error("Datos no proporcionados", http_status=400)
        return UsuarioService.crear_usuario(data)
    except Exception as e:
        return response_error(f"Error interno del servidor: {str(e)}", http_status=500)

@usuarios_bp.route('/inicio-sesion', methods=['POST'])
def inicio_sesion():
    """
    Endpoint para iniciar sesión.
    """
    try:
        data = request.get_json()
        if not data:
            return response_error("Datos no proporcionados", http_status=400)
        return UsuarioService.inicio_sesion(data)
    except Exception as e:
        return response_error(f"Error interno del servidor: {str(e)}", http_status=500)

@usuarios_bp.route('/token', methods=['POST'])
def cargar_token():
    """
    Endpoint para generar un nuevo token.
    """
    try:
        data = request.get_json()
        if not data or 'email' not in data:
            return response_error("El campo 'email' es obligatorio", http_status=400)
        return UsuarioService.cargar_token(data)
    except Exception as e:
        return response_error(f"Error interno del servidor: {str(e)}", http_status=500)
