from flask import Blueprint, request
from services.usuario_service import UsuarioService
from utils.interceptor import token_required
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

@usuarios_bp.route('/cerrar-sesion', methods=['POST'])
@token_required  
def cerrar_sesion():
    """
    Endpoint para cerrar sesión y destruir el token del usuario.
    """
    try:
        # Obtener el ID del usuario desde los query parameters
        usuario_id = request.args.get("usuario_id", type=int)
        if not usuario_id:
            return response_error("El parámetro 'usuario_id' es obligatorio", http_status=400)

        # Obtener el token del encabezado Authorization
        token = request.headers.get('Authorization').split('Bearer ')[-1]

        # Llamar al servicio para destruir el token
        return UsuarioService.destruir_token(usuario_id, token)
    except Exception as e:
        return response_error(f"Error interno del servidor: {str(e)}", http_status=500)
