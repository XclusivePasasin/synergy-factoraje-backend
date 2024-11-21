from flask import Blueprint, jsonify, request
from utils.metricas import metrica_factura
from datetime import datetime
from models.parametros import Parametro
from models.solicitudes import Solicitud
from utils.db import db

facturas_bp = Blueprint('factura', __name__)

def response_success(data, message="Operación exitosa", code=0, http_status=200):
    return jsonify({
        "data": data,
        "message": message,
        "code": code,
        "http_status": http_status
    }), http_status

def response_error(message, code=1, http_status=400):
    return jsonify({
        "data": None,
        "message": message,
        "code": code,
        "http_status": http_status
    }), http_status

@facturas_bp.route('/obtener-detalle-factura', methods=['POST'])
def obtener_detalle_factura():
    try:
        datos = request.json

        # Validamos que los campos requeridos estén presentes
        campos_principales = ['cliente', 'id_factura', 'fecha_otorgamiento', 'fecha_vencimiento', 'monto_factura']
        for campo in campos_principales:
            if campo not in datos:
                return response_error(f"El campo {campo} es obligatorio", http_status=422)

        # Verificar si el id_factura ya está registrado en la tabla solicitudes
        solicitud_existente = Solicitud.query.filter_by(id_factura=datos['id_factura']).first()
        if solicitud_existente:
            return response_error("La factura ya fue procesada", http_status=409)

        # Validamos las fechas
        try:
            fecha_vencimiento = datetime.strptime(datos['fecha_vencimiento'], "%d/%m/%Y")
        except ValueError:
            return response_error("Formato de fecha inválido. Use DD/MM/YYYY", http_status=422)

        fecha_actual = datetime.now()
        if fecha_actual > fecha_vencimiento:
            return response_error("El tiempo de otorgamiento ha expirado", http_status=422)

        dias = (fecha_vencimiento - fecha_actual).days
        if dias < 0:
            return response_error("La fecha de vencimiento ya pasó", http_status=422)

        parametro = Parametro.query.first()
        if not parametro:
            return response_error("No se encontró ningún parámetro en la tabla", http_status=500)

        try:
            interes_anual = float(parametro.valor)
        except ValueError:
            return response_error("El valor del parámetro de interés anual no es válido", http_status=500)

        resultado = metrica_factura(dias, datos['monto_factura'], interes_anual)

        resultado.update({
            "cliente": datos["cliente"],
            "id_factura": datos["id_factura"],
            "dias_restantes": dias,
            "fecha_otorgamiento": datos["fecha_otorgamiento"],
            "fecha_vencimiento": datos["fecha_vencimiento"],
            "monto_factura": datos["monto_factura"]
        })

        return response_success(resultado, "Detalle de factura obtenido correctamente", http_status=200)
    except Exception as e:
        return response_error(str(e), http_status=500)


@facturas_bp.route('/solicitar-pago-factura', methods=['POST'])
def solicitar_pago_factura():
    try:
        datos = request.json

        campos_principales = [
            'cliente', 'id_factura', 'fecha_otorgamiento', 'fecha_vencimiento',
            'monto_factura', 'contacto', 'email'
        ]
        for campo in campos_principales:
            if campo not in datos:
                return response_error(f"El campo {campo} es obligatorio", http_status=422)

        solicitud_existente = Solicitud.query.filter_by(id_factura=datos['id_factura']).first()
        if solicitud_existente:
            return response_error("La factura ya fue procesada", http_status=409)

        try:
            fecha_vencimiento = datetime.strptime(datos['fecha_vencimiento'], "%d/%m/%Y")
        except ValueError:
            return response_error("Formato de fecha inválido. Use DD/MM/YYYY", http_status=422)

        fecha_actual = datetime.now()
        if fecha_actual > fecha_vencimiento:
            return response_error("El tiempo de otorgamiento ha expirado", http_status=422)

        dias = (fecha_vencimiento - fecha_actual).days
        if dias < 0:
            return response_error("La fecha de vencimiento ya pasó", http_status=422)

        parametro = Parametro.query.first()
        if not parametro:
            return response_error("No se encontró ningún parámetro en la tabla", http_status=500)

        try:
            interes_anual = float(parametro.valor)
        except ValueError:
            return response_error("El valor del parámetro de interés anual no es válido", http_status=500)

        resultado = metrica_factura(dias, datos['monto_factura'], interes_anual)

        nueva_solicitud = Solicitud(
            nombre_cliente=datos['cliente'],
            contacto=datos['contacto'],
            email=datos['email'],
            descuento_app=resultado['pronto_pago'],
            iva=resultado['iva'],
            subtotal=resultado['subtotal_descuento'],
            total=resultado['total_a_recibir'],
            fecha_solicitud=fecha_actual,
            id_factura=datos['id_factura']
        )

        db.session.add(nueva_solicitud)
        db.session.commit()

        resultado.update({
            "cliente": datos["cliente"],
            "id_factura": datos["id_factura"],
            "dias_restantes": dias,
            "fecha_otorgamiento": datos["fecha_otorgamiento"],
            "fecha_vencimiento": datos["fecha_vencimiento"],
            "monto_factura": datos["monto_factura"],
            "contacto": datos["contacto"],
            "email": datos["email"]
        })

        return response_success(resultado, "Solicitud creada exitosamente", http_status=201)
    except Exception as e:
        return response_error(str(e), http_status=500)
