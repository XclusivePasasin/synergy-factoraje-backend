from flask import Blueprint, jsonify, request
from services.email_service import generar_plantilla, enviar_correo

email_bp = Blueprint('email', __name__)

@email_bp.route('/enviar-email', methods=['POST'])
def enviar_email():
    try:
        # Obtenemos JSON de la petición
        datos = request.json
        # Validamos que los campos requeridos estén presentes
        campos_principales = ['destinatario', 'asunto', 'datos']
        for campo in campos_principales:
            if campo not in datos:
                return jsonify({"error": f"El campo {campo} es obligatorio"}), 400
        # Validamos que los campos requeridos dentro de 'datos' estén presentes
        datos_plantilla = datos['datos']
        campos_datos = ['nombreEmpresa', 'noFactura', 'monto', 'fechaOtorgamiento', 'fechaVencimiento', 'diasCredito', 'linkBoton']
        for campo in campos_datos:
            if campo not in datos_plantilla:
                return jsonify({"error": f"El campo {campo} es obligatorio dentro de 'datos'"}), 400
        # Generamos el contenido HTML
        contenido_html = generar_plantilla(datos_plantilla)
        resultado = enviar_correo(datos['destinatario'], datos['asunto'], contenido_html)

        if resultado:
            return jsonify({"mensaje": "Correo enviado exitosamente"}), 200
        else:
            return jsonify({"error": "No se pudo enviar el correo"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# @email_bp.route('/obtener-metricas', methods=['POST'])