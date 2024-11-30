from flask import Flask, request, Blueprint
from utils.db import db
from models.solicitudes import Solicitud
from models.facturas import Factura
from models.comentarios import Comentario
from models.proveedores_calificados import ProveedorCalificado
from sqlalchemy import and_, or_
from utils.response import response_success, response_error
from utils.interceptor import token_required
from services.email_service import *

solicitud_bp = Blueprint('solicitud', __name__)

@solicitud_bp.route('/obtener-solicitudes', methods=['GET'])
@token_required
def obtener_solicitudes():
    try:
        # Obtener los parámetros de consulta
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))
        fecha_inicio = request.args.get('fecha_inicio')
        fecha_fin = request.args.get('fecha_fin')
        estado = request.args.get('estado')
        nombre_proveedor = request.args.get('nombre_proveedor')
        nrc = request.args.get('nrc')
        telefono = request.args.get('telefono')
        correo = request.args.get('correo')
        no_factura = request.args.get('no_factura')

        # Construir el query base
        query = db.session.query(Solicitud).join(Factura, Solicitud.id_factura == Factura.id).join(
            ProveedorCalificado, Factura.id_proveedor == ProveedorCalificado.id)

        # Filtros opcionales
        if fecha_inicio and fecha_fin:
            query = query.filter(Solicitud.fecha_solicitud.between(fecha_inicio, fecha_fin))
        if estado:
            query = query.filter(Solicitud.id_estado == estado)
        if nombre_proveedor:
            query = query.filter(ProveedorCalificado.razon_social.ilike(f"%{nombre_proveedor}%"))
        if nrc:
            query = query.filter(ProveedorCalificado.nrc.ilike(f"%{nrc}%"))
        if telefono:
            query = query.filter(ProveedorCalificado.telefono.ilike(f"%{telefono}%"))
        if correo:
            query = query.filter(ProveedorCalificado.correo_electronico.ilike(f"%{correo}%"))
        if no_factura:  
            query = query.filter(Factura.no_factura.ilike(f"%{no_factura}%"))

        # Paginación
        total_solicitudes = query.count()
        solicitudes = query.offset((page - 1) * per_page).limit(per_page).all()

        # Construir la respuesta
        response_data = {
            "current_page": page,
            "per_page": per_page,
            "total_pages": (total_solicitudes + per_page - 1) // per_page,
            "solicitudes": [
                {
                    "id": solicitud.id,
                    "nombre_cliente": solicitud.nombre_cliente,
                    "contacto": solicitud.contacto,
                    "email": solicitud.email,
                    "iva": float(solicitud.iva),
                    "subtotal": float(solicitud.subtotal),
                    "total": float(solicitud.total),
                    "estado": solicitud.estado.clave ,
                    "id_estado": solicitud.id_estado,
                    "factura": {
                        "id": solicitud.factura.id,
                        "no_factura": solicitud.factura.no_factura,
                        "monto": float(solicitud.factura.monto),
                        "fecha_emision": solicitud.factura.fecha_emision.isoformat(),
                        "fecha_vence": solicitud.factura.fecha_vence.isoformat(),
                        "fecha_otorga": solicitud.factura.fecha_otorga.isoformat(),
                        "proveedor": {
                            key: getattr(solicitud.factura.proveedor, key)
                            for key in ProveedorCalificado.__table__.columns.keys()
                            if key not in ["cuenta_bancaria", "created_at", "updated_at"]
                        }
                    } if solicitud.factura else None
                } for solicitud in solicitudes
            ]
        }

        return response_success(response_data, "Consulta exitosa")
    except Exception as e:
        return response_error(f"Error al procesar la solicitud: {str(e)}", http_status=500)
    
@solicitud_bp.route('/obtener-detalle-solicitud', methods=['GET'])
@token_required
def obtener_detalle_solicitud():
    try:
        # Obtener el parámetro `id` de la solicitud desde la URL
        solicitud_id = request.args.get('id', type=int)
        
        if not solicitud_id:
            return response_error("El parámetro 'id' es obligatorio", http_status=400)

        # Buscar la solicitud por ID
        solicitud = db.session.query(Solicitud).filter_by(id=solicitud_id).first()

        if not solicitud:
            return response_error("La solicitud no existe", http_status=404)

        # Construir los datos de respuesta
        solicitud_data = {
            "id": solicitud.id,
            "nombre_cliente": solicitud.nombre_cliente,
            "contacto": solicitud.contacto,
            "email": solicitud.email,
            "iva": float(solicitud.iva),
            "subtotal": float(solicitud.subtotal),
            "total": float(solicitud.total),
            "estado": solicitud.estado.clave if solicitud.estado else None,
            "id_estado": solicitud.id_estado,
            "factura": {
                "id": solicitud.factura.id,
                "no_factura": solicitud.factura.no_factura,
                "monto": float(solicitud.factura.monto),
                "fecha_emision": solicitud.factura.fecha_emision.isoformat(),
                "fecha_vence": solicitud.factura.fecha_vence.isoformat(),
                "proveedor": {
                    "id": solicitud.factura.proveedor.id,
                    "razon_social": solicitud.factura.proveedor.razon_social,
                    "correo_electronico": solicitud.factura.proveedor.correo_electronico,
                    "telefono": solicitud.factura.proveedor.telefono,
                }
            } if solicitud.factura else None
        }

        return response_success(solicitud_data, "Consulta exitosa")
    except Exception as e:
        return response_error(f"Error al procesar la solicitud: {str(e)}", http_status=500)
    
@solicitud_bp.route('/aprobar', methods=['PUT'])
@token_required
def aprobar_solicitud():
    try:
        # Obtener el ID de la solicitud desde los query parameters
        solicitud_id = request.args.get('id', type=int)
        if not solicitud_id:
            return response_error("El parámetro 'id' es obligatorio", http_status=400)

        # Obtener datos del body
        data = request.get_json()
        id_aprobador = data.get('id_aprobador')  
        comentario = data.get('comentario', None)

        if not id_aprobador:
            return response_error("El campo 'id_aprobador' es obligatorio", http_status=400)

        # Buscar la solicitud por ID
        solicitud = db.session.query(Solicitud).filter_by(id=solicitud_id).first()
        if not solicitud:
            return response_error("La solicitud no existe", http_status=404)

        # Validar si la solicitud ya está aprobada
        if solicitud.id_estado == 2:  
            return response_success(None, "La solicitud ya fue aprobada. No se realizó ningún cambio.")

        # Actualizar el estado de la solicitud
        solicitud.id_estado = 2  
        solicitud.fecha_aprobacion = db.func.now()
        solicitud.id_aprobador = id_aprobador  

        # Registrar comentario si se proporciona
        if comentario:
            nuevo_comentario = Comentario(
                id_solicitud=solicitud_id,
                comentario=comentario,
                created_at=db.func.now(),
                updated_at=db.func.now()
            )
            db.session.add(nuevo_comentario)

        # Guardar cambios en la base de datos
        db.session.commit()

        # Enviar correo al usuario notificando la aprobación
        datos_aprobacion = {
            "nombreSolicitante": solicitud.nombre_cliente,
            "noFactura": solicitud.factura.no_factura,
            "montoFactura": f"${solicitud.total:.2f}",
            "descuento": f"${solicitud.descuento_app:.2f}",
            "iva": f"${solicitud.iva:.2f}",
            "subtotal": f"${solicitud.subtotal:.2f}",
            "fechaSolicitud": solicitud.fecha_solicitud.strftime("%d/%m/%Y"),
            "fechaVencimiento": solicitud.factura.fecha_vence.strftime("%d/%m/%Y"),
            "diasCredito": (solicitud.factura.fecha_vence - solicitud.fecha_aprobacion).days
        }
        asunto = f"Solicitud de Pronto Pago Aprobada FACTURA {datos_aprobacion['noFactura']}"
        contenido_html_aprobacion = generar_plantilla('correo_aprobacion_solicitud_pp.html', datos_aprobacion)

        # Enviar correo al cliente
        enviar_correo(solicitud.email, asunto, contenido_html_aprobacion)

        # Construir respuesta
        solicitud_data = {
            "id": solicitud.id,
            "nombre_cliente": solicitud.nombre_cliente,
            "contacto": solicitud.contacto,
            "email": solicitud.email,
            "id_estado": solicitud.id_estado,
            "id_aprobador": solicitud.id_aprobador,  
            "fecha_aprobacion": solicitud.fecha_aprobacion.isoformat() if solicitud.fecha_aprobacion else None,
            "total": float(solicitud.total),
            "factura": {
                "id": solicitud.factura.id,
                "no_factura": solicitud.factura.no_factura,
                "monto": float(solicitud.factura.monto),
                "proveedor": {
                    "id": solicitud.factura.proveedor.id,
                    "razon_social": solicitud.factura.proveedor.razon_social
                }
            } if solicitud.factura else None
        }

        return response_success({"solicitud": solicitud_data}, "Solicitud aprobada exitosamente. Correo de notificación enviado.")
    except Exception as e:
        return response_error(f"Error al procesar la solicitud: {str(e)}", http_status=500)




@solicitud_bp.route('/desaprobar', methods=['PUT'])
@token_required
def desaprobar_solicitud():
    try:
        # Obtener el ID de la solicitud desde los query parameters
        solicitud_id = request.args.get('id', type=int)
        if not solicitud_id:
            return response_error("El parámetro 'id' es obligatorio", http_status=400)

        # Obtener datos del body
        data = request.get_json()
        comentario = data.get('comentario', None)

        # Buscar la solicitud por ID
        solicitud = db.session.query(Solicitud).filter_by(id=solicitud_id).first()
        if not solicitud:
            return response_error("La solicitud no existe", http_status=404)

        # Validar si la solicitud ya está denegada
        if solicitud.id_estado == 3:  
            return response_success(None, "La solicitud ya fue denegada. No se realizó ningún cambio.")

        # Actualizar el estado de la solicitud
        solicitud.id_estado = 3  
        solicitud.fecha_aprobacion = None  

        # Registrar comentario si se proporciona
        if comentario:
            nuevo_comentario = Comentario(
                id_solicitud=solicitud_id,
                comentario=comentario,
                created_at=db.func.now(),
                updated_at=db.func.now()
            )
            db.session.add(nuevo_comentario)

        # Guardar cambios en la base de datos
        db.session.commit()

        # Enviar correo al usuario notificando la denegación
        datos_denegacion = {
            "nombreSolicitante": solicitud.nombre_cliente,
            "noFactura": solicitud.factura.no_factura,
            "montoFactura": f"${solicitud.total:.2f}",
            "fechaSolicitud": solicitud.fecha_solicitud.strftime("%d/%m/%Y"),
        }
        asunto = f"Solicitud de Pronto Pago Denegada FACTURA {datos_denegacion['noFactura']}"
        contenido_html_denegacion = generar_plantilla('correo_denegacion_solicitud_pp.html', datos_denegacion)

        # Enviar correo al cliente
        enviar_correo(solicitud.email, asunto, contenido_html_denegacion)

        # Construir respuesta
        solicitud_data = {
            "id": solicitud.id,
            "nombre_cliente": solicitud.nombre_cliente,
            "contacto": solicitud.contacto,
            "email": solicitud.email,
            "id_estado": solicitud.id_estado,
            "total": float(solicitud.total),
            "factura": {
                "id": solicitud.factura.id,
                "no_factura": solicitud.factura.no_factura,
                "monto": float(solicitud.factura.monto),
                "proveedor": {
                    "id": solicitud.factura.proveedor.id,
                    "razon_social": solicitud.factura.proveedor.razon_social
                }
            } if solicitud.factura else None
        }

        return response_success({"solicitud": solicitud_data}, "Solicitud denegada exitosamente. Correo de notificación enviado.")
    except Exception as e:
        return response_error(f"Error al procesar la solicitud: {str(e)}", http_status=500)



