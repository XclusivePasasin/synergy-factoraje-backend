from flask import Blueprint, request
from sqlalchemy import or_, and_
from utils.db import db
from utils.response import response_success, response_error
from models import Solicitud, Desembolso, Factura, ProveedorCalificado
from utils.interceptor import token_required

desembolsos_bp = Blueprint('desembolso', __name__)

@desembolsos_bp.route('/obtener-desembolsos', methods=['GET'])
@token_required
def obtener_desembolsos():
    try:
        # Recuperar parámetros de consulta
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        fecha_inicio = request.args.get('fecha_inicio', type=str)
        fecha_fin = request.args.get('fecha_fin', type=str)
        estado = request.args.get('estado', type=str)
        proveedor = request.args.get('proveedor', type=str)

        # Construcción de filtros dinámicos
        query = Desembolso.query.join(Solicitud).join(Factura).join(ProveedorCalificado)

        if fecha_inicio and fecha_fin:
            query = query.filter(Desembolso.fecha_desembolso.between(fecha_inicio, fecha_fin))
        if estado:
            query = query.filter(Desembolso.estado.ilike(f"%{estado}%"))
        if proveedor:
            query = query.filter(
                or_(
                    ProveedorCalificado.razon_social.ilike(f"%{proveedor}%"),
                    ProveedorCalificado.correo_electronico.ilike(f"%{proveedor}%"),
                    ProveedorCalificado.nrc.ilike(f"%{proveedor}%"),
                    ProveedorCalificado.telefono.ilike(f"%{proveedor}%")
                )
            )

        # Aplicar paginación
        paginated_query = query.paginate(page=page, per_page=per_page, error_out=False)
        desembolsos = paginated_query.items

        # Construir la respuesta
        response_data = {
            "current_page": paginated_query.page,
            "per_page": paginated_query.per_page,
            "total_pages": paginated_query.pages,
            "solicitudes": [
                {
                    "id": desembolso.id,
                    "fecha_desembolso": desembolso.fecha_desembolso.isoformat(),
                    "monto_final": float(desembolso.monto_final),
                    "metodo_pago": desembolso.metodo_pago,
                    "estado": desembolso.estado,
                    "solicitud": {
                        "id": desembolso.solicitud.id,
                        "nombre_cliente": desembolso.solicitud.nombre_cliente,
                        "contacto": desembolso.solicitud.contacto,
                        "email": desembolso.solicitud.email,
                        "iva": float(desembolso.solicitud.iva),
                        "subtotal": float(desembolso.solicitud.subtotal),
                        "total": float(desembolso.solicitud.total),
                        "estado": desembolso.solicitud.estado.estado,
                        "factura": {
                            "id": desembolso.solicitud.factura.id,
                            "no_factura": desembolso.solicitud.factura.no_factura,
                            "monto": float(desembolso.solicitud.factura.monto),
                            "fecha_emision": desembolso.solicitud.factura.fecha_emision.isoformat(),
                            "fecha_vence": desembolso.solicitud.factura.fecha_vence.isoformat(),
                            "proveedor": {
                                "id": desembolso.solicitud.factura.proveedor.id,
                                "razon_social": desembolso.solicitud.factura.proveedor.razon_social,
                                "correo_electronico": desembolso.solicitud.factura.proveedor.correo_electronico,
                                "telefono": desembolso.solicitud.factura.proveedor.telefono
                            }
                        }
                    }
                } for desembolso in desembolsos
            ]
        }

        return response_success(response_data, "Consulta exitosa")

    except Exception as e:
        return response_error(f"Error al consultar desembolsos: {str(e)}", http_status=500)
    
@desembolsos_bp.route('/detalle-desembolso', methods=['GET'])
@token_required
def obtener_detalle_desembolso():
    try:
        # Recuperar el ID de la solicitud desde los parámetros de consulta
        solicitud_id = request.args.get('solicitud_id', type=int)
        
        if not solicitud_id:
            return response_error("El parámetro 'solicitud_id' es requerido", http_status=400)

        # Buscar el desembolso relacionado con la solicitud
        desembolso = Desembolso.query.join(Solicitud).join(Factura).join(ProveedorCalificado).filter(
            Desembolso.id_solicitud == solicitud_id
        ).first()

        if not desembolso:
            return response_error("Desembolso no encontrado para la solicitud indicada", http_status=404)

        # Construir la respuesta detallada
        response_data = {
            "desembolso": {
                "id": desembolso.id,
                "fecha_desembolso": desembolso.fecha_desembolso.isoformat(),
                "monto_final": float(desembolso.monto_final),
                "metodo_pago": desembolso.metodo_pago,
                "no_transaccion": desembolso.no_transaccion,
                "estado": desembolso.estado,
                "proveedor": {
                    "id": desembolso.solicitud.factura.proveedor.id,
                    "razon_social": desembolso.solicitud.factura.proveedor.razon_social,
                    "correo_electronico": desembolso.solicitud.factura.proveedor.correo_electronico,
                    "telefono": desembolso.solicitud.factura.proveedor.telefono
                }
            }
        }

        return response_success(response_data, "Consulta exitosa")

    except Exception as e:
        return response_error(f"Error al obtener el detalle del desembolso: {str(e)}", http_status=500)
    