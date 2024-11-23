from flask.cli import AppGroup
from extensions import db
from models.parametros import Parametro
from models.estados import Estado

# Crear un grupo de comandos para seeds
seed_cli = AppGroup('seed')

@seed_cli.command('parametros')
def seed_parametros():
    parametros = [
        {"clave": "INT_AN_PP", "valor": "12.5"},
        {"clave": "OTRO_PARAM", "valor": "Valor por defecto"}
    ]

    for param_data in parametros:
        parametro = Parametro.query.filter_by(clave=param_data["clave"]).first()
        if not parametro:
            parametro = Parametro(**param_data)
            db.session.add(parametro)
    db.session.commit()
    print("Seeds para 'parametros' creados exitosamente.")

@seed_cli.command('estados')
def seed_estados():
    estados = [
        {
            "clave": "PENDIENTE",
            "descripcion": "Estado de la factura cuando se ha enviado por correo al proveedor clasificado para pronto pago",
            "clasificacion": "Solicitud"
        },
        {
            "clave": "SOLICITADA",
            "descripcion": "Estado de una solicitud cuando el proveedor decide factoraje",
            "clasificacion": "Solicitud"
        },
        {
            "clave": "APROBADA",
            "descripcion": "Estado de la solicitud cuando ya ha sido aprobada por un agente de Synergy",
            "clasificacion": "Solicitud"
        },
        {
            "clave": "DENEGADA",
            "descripcion": "Estado de la solicitud cuando ya ha sido denegada por un agente de Synergy",
            "clasificacion": "Solicitud"
        },
        {
            "clave": "DESEMBOLSADA",
            "descripcion": "Estado que indica que el desembolso se ha hecho correctamente al proveedor que aplicó a pronto pago",
            "clasificacion": "Solicitud"
        }
    ]

    for estado_data in estados:
        estado = Estado.query.filter_by(clave=estado_data["clave"]).first()
        if not estado:
            estado = Estado(**estado_data)
            db.session.add(estado)
    db.session.commit()
    print("Seeds para 'estados' creados exitosamente.")

@seed_cli.command('all')
def seed_all():
    """Ejecuta todos los comandos de seeds"""
    print("Iniciando el seed de todas las tablas...")
    seed_parametros()
    seed_estados()
    print("Seeds ejecutados correctamente en todas las tablas.")

def init_app(app):
    app.cli.add_command(seed_cli)
