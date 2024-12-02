from flask import Blueprint, request
from utils.metricas import metrica_factura
from datetime import datetime
from models.parametros import Parametro
from models.solicitudes import Solicitud
from models.facturas import Factura
from utils.db import db
from utils.response import response_success, response_error
from utils.interceptor import token_required
from services.email_service import *

facturas_bp = Blueprint('factura', __name__)

@facturas_bp.route('/obtener-detalle-factura', methods=['GET'])
@token_required
def obtener_detalle_factura():
    try:
        # Obtener el parámetro no_factura desde la URL
        no_factura = request.args.get('no_factura')
        if not no_factura:
            return response_error("El parámetro no_factura es obligatorio", http_status=422)

        # Consulta para obtener los detalles de la factura
        factura = Factura.query.filter_by(no_factura=no_factura).first()
        if not factura:
            return response_error(f"No se encontró una factura con el número: {no_factura}", http_status=404)

        # Calcular los días restantes para el vencimiento
        fecha_actual = datetime.now()
        dias_restantes = (factura.fecha_vence - fecha_actual).days
        if dias_restantes < 0:
            return response_error("La fecha de vencimiento ya pasó", http_status=422)

        # Obtener el parámetro de interés anual
        parametro = Parametro.query.filter_by(clave='INT_AN_PP').first()
        if not parametro:
            return response_error("No se encontró ningún parámetro en la tabla", http_status=500)

        try:
            interes_anual = float(parametro.valor)
        except ValueError:
            return response_error("El valor del parámetro de interés anual no es válido", http_status=500)

        # Calcular la métrica con los datos obtenidos
        resultado = metrica_factura(dias_restantes, float(factura.monto), interes_anual)

        # Preparar los detalles de la factura dentro del nodo "facturas"
        resultado_final = {
            "factura": {
                "cliente": factura.nombre_proveedor,
                "no_factura": factura.no_factura,
                "dias_restantes": dias_restantes,
                "fecha_otorgamiento": factura.fecha_otorga.strftime("%d/%m/%Y"),
                "fecha_vencimiento": factura.fecha_vence.strftime("%d/%m/%Y"),
                "monto_factura": float(factura.monto),
                **resultado  # Incluye los cálculos realizados por metrica_factura
            }
        }

        return response_success(resultado_final, "Detalle de factura obtenido correctamente", http_status=200)
    except Exception as e:
        return response_error(str(e), http_status=500)

@facturas_bp.route('/solicitar-pago-factura', methods=['POST'])
@token_required
def solicitar_pago_factura():
    try:
        datos = request.json

        # Validar que el nodo "data" y "factura" existan en el JSON
        if 'data' not in datos or 'factura' not in datos['data']:
            return response_error("El nodo 'data.factura' es obligatorio", http_status=422)

        data = datos['data']

        # Validar los campos adicionales dentro de "data"
        campos_adicionales = ['nombre_solicitante', 'cargo', 'correo_electronico']
        for campo in campos_adicionales:
            if campo not in data:
                return response_error(f"El campo {campo} en 'data' es obligatorio", http_status=422)

        # Validar los campos requeridos dentro de "factura"
        facturas_data = data['factura']
        campos_factura = [
            'cliente', 'no_factura', 'fecha_otorgamiento', 'fecha_vencimiento',
            'monto_factura', 'iva', 'pronto_pago', 'subtotal_descuento', 'total_a_recibir'
        ]
        for campo in campos_factura:
            if campo not in facturas_data:
                return response_error(f"El campo {campo} en 'factura' es obligatorio", http_status=422)

        # Validar que la factura exista por no_factura
        factura_existente = Factura.query.filter_by(no_factura=facturas_data['no_factura']).first()
        if not factura_existente:
            return response_error("La solicitud proporcionada no existe en la base de datos", http_status=422)

        # Validar que la solicitud no exista ya para esa factura
        solicitud_existente = Solicitud.query.filter_by(id_factura=factura_existente.id).first()
        if solicitud_existente:
            return response_error("La solicitud ya fue procesada", http_status=409)

        # Validar formato de fecha
        try:
            fecha_vencimiento = datetime.strptime(facturas_data['fecha_vencimiento'], "%d/%m/%Y")
        except ValueError:
            return response_error("Formato de fecha inválido. Use DD/MM/YYYY", http_status=422)

        fecha_actual = datetime.now()
        if fecha_actual > fecha_vencimiento:
            return response_error("El tiempo de otorgamiento ha expirado", http_status=422)

        dias = (fecha_vencimiento - fecha_actual).days
        if dias < 0:
            return response_error("La fecha de vencimiento ya pasó", http_status=422)

        # Crear la nueva solicitud
        nueva_solicitud = Solicitud(
            nombre_cliente=data['nombre_solicitante'],  
            contacto=factura_existente.proveedor.telefono,  
            email=data['correo_electronico'],
            cargo=data['cargo'],
            descuento_app=facturas_data['pronto_pago'],
            iva=facturas_data['iva'],
            subtotal=facturas_data['subtotal_descuento'],
            total=facturas_data['total_a_recibir'],
            fecha_solicitud=fecha_actual,
            id_factura=factura_existente.id,
            id_estado=1  
        )

        db.session.add(nueva_solicitud)
        db.session.commit()

        # Obtener los parámetros adicionales de la base de datos
        parametros = Parametro.query.filter(Parametro.clave.in_(['NOM-EMPRESA', 'ENC-EMPRESA', 'TEL-EMPRESA','MAIL-EMPRESA'])).all()
        parametros_dict = {param.clave: param.valor for param in parametros}

        nombre_empresa = parametros_dict.get('NOM-EMPRESA', 'Nombre Empresa No Definido')
        nombre_encargado = parametros_dict.get('ENC-EMPRESA', 'Encargado No Definido')
        telefono_empresa = parametros_dict.get('TEL-EMPRESA', 'Teléfono No Definido')
        email_empresa = parametros_dict.get('MAIL-EMPRESA', 'Email No Definido')

        # Datos para el correo de confirmación al proveedor
        datos_confirmacion = {
            "nombreSolicitante": data['nombre_solicitante'],
            "noFactura": facturas_data['no_factura'],
            "monto": f"${facturas_data['monto_factura']}",
            "fechaSolicitud": fecha_actual.strftime("%d/%m/%Y"),
            "nombreEmpresa": nombre_empresa,
            "nombreEncargadoEmpresa": nombre_encargado,
            "telefonoEmpresa": telefono_empresa,
        }
        asunto_confirmacion = f"Confirmación de Recepción de su Solicitud de Pronto Pago FACTURA {datos_confirmacion['noFactura']}"
        contenido_html_confirmacion = generar_plantilla('correo_confirmacion_solicitud_pp.html', datos_confirmacion)

        # Enviar correo de confirmación al proveedor
        enviar_correo(data['correo_electronico'], asunto_confirmacion, contenido_html_confirmacion)

        # Datos para el correo de notificación a Synergy
        datos_notificacion = {
            "nombreEmpresa": nombre_empresa,
            "proveedor": facturas_data['cliente'],
            "noFactura": facturas_data['no_factura'],
            "montoFactura": f"${facturas_data['monto_factura']}",
            "fechaSolicitud": fecha_actual.strftime("%d/%m/%Y"),
            "diasCredito": dias,
            "nombreEmpresa": nombre_empresa
        }
        asunto_notificacion = f"Nueva Solicitud de Pronto Pago en Espera de Gestión FACTURA {datos_notificacion['noFactura']}"
        contenido_html_notificacion = generar_plantilla('correo_notificacion_solicitud_pendiente_aprobacion_pp.html', datos_notificacion)

        # Enviar correo de notificación a Synergy
        enviar_correo(email_empresa, asunto_notificacion, contenido_html_notificacion)

        return response_success("Solicitud creada exitosamente. Los correos de confirmación y notificación han sido enviados.", http_status=201)
    except Exception as e:
        return response_error(str(e), http_status=500)




