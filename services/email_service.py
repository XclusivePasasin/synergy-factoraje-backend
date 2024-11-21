import os
from jinja2 import Environment, FileSystemLoader
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import Config

# Configuración del entorno de plantillas
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(BASE_DIR, '../templates')
env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))

def generar_plantilla(datos):
    template = env.get_template('correo_template.html')
    return template.render(
        nombreEmpresa=datos["nombreEmpresa"],
        noFactura=datos["noFactura"],
        monto=datos["monto"],
        fechaOtorgamiento=datos["fechaOtorgamiento"],
        fechaVencimiento=datos["fechaVencimiento"],
        diasCredito=datos["diasCredito"],
        linkBoton=datos["linkBoton"]
    )

def enviar_correo(destinatario, asunto, contenido_html):
    try:
        servidor = smtplib.SMTP(Config.MAIL_SERVER, Config.MAIL_PORT)
        servidor.starttls()
        servidor.login(Config.MAIL_USERNAME, Config.MAIL_PASSWORD)

        mensaje = MIMEMultipart()
        mensaje['From'] = Config.MAIL_USERNAME
        mensaje['To'] = destinatario
        mensaje['Subject'] = asunto
        mensaje.attach(MIMEText(contenido_html, 'html'))
        # Enviar el correo
        servidor.send_message(mensaje)
        servidor.quit()
        return True
    except Exception as e:
        print(f"Error al enviar el correo: {e}")
        return False

