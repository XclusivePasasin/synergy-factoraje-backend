from flask import Blueprint, request
from services.proveedores_service import *
from utils.response import response_success, response_error
from utils.interceptor import token_required
import logging

proveedor_bp = Blueprint('proveedor', __name__)

@proveedor_bp.route('/proveedor/registrar', methods=['POST'])
@token_required
def registrar_proveedor():
    try:
        data = request.get_json()
        if not data:
            return response_error("El cuerpo de la solicitud está vacío", http_status=400)

        # Validación de campos obligatorios
        campos_obligatorios = [
            'id', 'razon_social', 'nrc', 'nit', 'correo_electronico', 'cuenta_bancaria', 'min_factoring', 'max_factoring', 'banco', 'codigo_banco', 'nombre_contacto', 'telefono'
        ]
        faltantes = [campo for campo in campos_obligatorios if campo not in data]
        if faltantes:
            return response_error(f"Faltan los campos obligatorios: {', '.join(faltantes)}", http_status=400)

        # Llamar al servicio
        proveedor = crear_proveedor(data)
        return response_success(proveedor, "Proveedor creado exitosamente")

    except ValueError as e:
        return response_error(str(e), http_status=400)
    except Exception as e:
        return response_error("Error interno del servidor", http_status=500)

@proveedor_bp.route('/proveedor/obtener-proveedor', methods=['GET'])
@token_required
def obtener_proveedor():
    try:
        id = request.args.get('id')  # Obtener ID desde query param
        
        if not id:
            return response_error("El ID del proveedor es obligatorio como query param (?id=...)", http_status=400)

        proveedor = obtener_proveedor_service(id)
        return response_success(proveedor, "Proveedor obtenido exitosamente")

    except ValueError as e:
        logging.warning(f"Error de validación al obtener proveedor: {e}")
        return response_error(str(e), http_status=404)

    except Exception as e:
        logging.error(f"Error inesperado al obtener proveedor: {e}", exc_info=True)
        return response_error("Error interno del servidor", http_status=500)
    
@proveedor_bp.route('/proveedor/actualizar', methods=['PUT'])
@token_required
def modificar_proveedor():
    try:
        id = request.args.get('id')  
        
        if not id:
            return response_error("El ID del proveedor es obligatorio como query param (?id=...)", http_status=400)

        data = request.get_json()
        if not data:
            return response_error("El cuerpo de la solicitud está vacío", http_status=400)

        proveedor_actualizado = actualizar_proveedor(id, data)
        return response_success(proveedor_actualizado, "Proveedor actualizado exitosamente")

    except ValueError as e:
        return response_error(str(e), http_status=400)

    except Exception as e:
        return response_error("Error interno del servidor", http_status=500)
    
@proveedor_bp.route('/proveedor/eliminar', methods=['DELETE'])
@token_required
def suprimir_proveedor():
    try:
        id = request.args.get('id')  # Obtener ID desde query param

        if not id:
            return response_error("El ID del proveedor es obligatorio como query param (?id=...)", http_status=400)

        eliminar_proveedor(id)
        return response_success(None, "Proveedor eliminado exitosamente")

    except ValueError as e:
        logging.warning(f"Error de validación al eliminar proveedor: {e}")
        return response_error(str(e), http_status=404)

    except Exception as e:
        logging.error(f"Error inesperado al eliminar proveedor: {e}", exc_info=True)
        return response_error("Error interno del servidor", http_status=500)

@proveedor_bp.route('/proveedor/listar', methods=['GET'])
@token_required
def obtener_proveedores():
    try:
        proveedores = listar_proveedores()
        return response_success(proveedores, "Lista de proveedores obtenida exitosamente")

    except Exception as e:
        logging.error(f"Error inesperado al listar proveedores: {e}", exc_info=True)
        return response_error("Error interno del servidor", http_status=500)