from flask.cli import AppGroup
from flask import current_app
from extensions import db
from models.parametros import Parametro
from models.estados import Estado
from models.proveedores_calificados import ProveedorCalificado
from models.facturas import Factura
from models.roles import Rol

# Crear un grupo de comandos para seeds
seed_cli = AppGroup('seed')

@seed_cli.command('parametros')
def seed_parametros():
    """Seed de parámetros"""
    with current_app.app_context():
        parametros = [
            {"clave": "INT_AN_PP", "valor": "18"},
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
    """Seed de estados"""
    with current_app.app_context():
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

@seed_cli.command('roles')
def seed_roles():
    """Seed de roles"""
    with current_app.app_context():
        roles = [
            {
                "rol": "Administrador",
                "nombre": "Administrador",
                "descripcion": None
            }
        ]

        for rol_data in roles:
            rol = Rol.query.filter_by(rol=rol_data["rol"]).first()
            if not rol:
                rol = Rol(**rol_data)
                db.session.add(rol)
        db.session.commit()
        print("Seeds para 'roles' creados exitosamente.")

@seed_cli.command('proveedores')
def seed_proveedores():
    """Seed de proveedores calificados"""
    with current_app.app_context():
        proveedores = [
            {
                "razon_social": "TechNova Solutions S.A.",
                "nrc": "NRC12345",
                "nit": "NIT456789123",
                "min_factoring": 1000.00,
                "max_factoring": 5000.00,
                "cuenta_bancaria": "1234567890",
                "nombre_contacto": "Juan Pérez",
                "correo_electronico": "contacto@technova.com",
                "telefono": "555-12345"
            },
            {
                "razon_social": "FutureTech Innovators",
                "nrc": "NRC67891",
                "nit": "NIT987654321",
                "min_factoring": 2000.00,
                "max_factoring": 8000.00,
                "cuenta_bancaria": "2233445566",
                "nombre_contacto": "Sofía Ramírez",
                "correo_electronico": "info@futuretech.com",
                "telefono": "555-67891"
            },
            {
                "razon_social": "AlphaOmega Services Ltd.",
                "nrc": "NRC33322",
                "nit": "NIT111222333",
                "min_factoring": 3000.00,
                "max_factoring": 10000.00,
                "cuenta_bancaria": "5566778899",
                "nombre_contacto": "Carlos Vega",
                "correo_electronico": "contact@alphaomega.com",
                "telefono": "555-33322"
            },
            {
                "razon_social": "NextWave IT Solutions",
                "nrc": "NRC98765",
                "nit": "NIT789654321",
                "min_factoring": 1500.00,
                "max_factoring": 9000.00,
                "cuenta_bancaria": "7788990011",
                "nombre_contacto": "Luis Gómez",
                "correo_electronico": "luis@nextwave.com",
                "telefono": "555-98765"
            },
            {
                "razon_social": "DigitalGenio Tech",
                "nrc": "NRC24680",
                "nit": "NIT246802468",
                "min_factoring": 2500.00,
                "max_factoring": 12000.00,
                "cuenta_bancaria": "3322114455",
                "nombre_contacto": "Ana Torres",
                "correo_electronico": "ana@digitalgenio.com",
                "telefono": "555-24680"
            },
            {
                "razon_social": "Quantum Leap Solutions",
                "nrc": "NRC13579",
                "nit": "NIT135791357",
                "min_factoring": 500.00,
                "max_factoring": 7000.00,
                "cuenta_bancaria": "5544332211",
                "nombre_contacto": "Miguel Pérez",
                "correo_electronico": "miguel@quantumleap.com",
                "telefono": "555-13579"
            },
            {
                "razon_social": "Nova Innovators S.A.",
                "nrc": "NRC44455",
                "nit": "NIT444555666",
                "min_factoring": 1000.00,
                "max_factoring": 5000.00,
                "cuenta_bancaria": "6677889900",
                "nombre_contacto": "Mónica López",
                "correo_electronico": "monica@novainnovators.com",
                "telefono": "555-44455"
            }
        ]

        for proveedor_data in proveedores:
            proveedor = ProveedorCalificado.query.filter_by(nrc=proveedor_data["nrc"]).first()
            if not proveedor:
                proveedor = ProveedorCalificado(**proveedor_data)
                db.session.add(proveedor)
        db.session.commit()
        print("Seeds para 'proveedores_calificados' creados exitosamente.")
        
@seed_cli.command('facturas')
def seed_facturas():
    """Seed de facturas"""
    with current_app.app_context():
        facturas = [
            {
                "no_factura": "FAC001",
                "monto": 1500.00,
                "fecha_emision": "2024-11-01 10:00:00",
                "fecha_vence": "2025-01-18 10:00:00",
                "fecha_otorga": "2024-11-01 11:00:00",
                "dias_credito": 78,
                "nombre_proveedor": "TechNova Solutions S.A.",
                "nit": "NIT456789123",
                "id_proveedor": 1
            },
            {
                "no_factura": "FAC002",
                "monto": 3000.00,
                "fecha_emision": "2024-11-05 09:00:00",
                "fecha_vence": "2025-01-19 09:00:00",
                "fecha_otorga": "2024-11-05 09:30:00",
                "dias_credito": 75,
                "nombre_proveedor": "CodeFusion Labs",
                "nit": "NIT123456789",
                "id_proveedor": 2
            },
            {
                "no_factura": "FAC003",
                "monto": 4500.00,
                "fecha_emision": "2024-11-10 08:30:00",
                "fecha_vence": "2025-02-01 08:30:00",
                "fecha_otorga": "2024-11-10 09:00:00",
                "dias_credito": 83,
                "nombre_proveedor": "FutureTech Innovators",
                "nit": "NIT987654321",
                "id_proveedor": 3
            },
            {
                "no_factura": "FAC004",
                "monto": 2000.00,
                "fecha_emision": "2024-11-12 10:00:00",
                "fecha_vence": "2025-02-12 10:00:00",
                "fecha_otorga": "2024-11-12 11:00:00",
                "dias_credito": 90,
                "nombre_proveedor": "AlphaOmega Services Ltd.",
                "nit": "NIT111222333",
                "id_proveedor": 4
            },
            {
                "no_factura": "FAC005",
                "monto": 3500.00,
                "fecha_emision": "2024-11-15 09:00:00",
                "fecha_vence": "2025-01-30 09:00:00",
                "fecha_otorga": "2024-11-15 10:00:00",
                "dias_credito": 76,
                "nombre_proveedor": "NextWave IT Solutions",
                "nit": "NIT789654321",
                "id_proveedor": 5
            },
            {
                "no_factura": "FAC006",
                "monto": 1200.00,
                "fecha_emision": "2024-11-18 14:00:00",
                "fecha_vence": "2025-02-05 14:00:00",
                "fecha_otorga": "2024-11-18 15:00:00",
                "dias_credito": 79,
                "nombre_proveedor": "DigitalGenio Tech",
                "nit": "NIT246802468",
                "id_proveedor": 6
            },
            {
                "no_factura": "FAC007",
                "monto": 5000.00,
                "fecha_emision": "2024-11-20 11:00:00",
                "fecha_vence": "2025-03-01 11:00:00",
                "fecha_otorga": "2024-11-20 12:00:00",
                "dias_credito": 100,
                "nombre_proveedor": "Quantum Leap Solutions",
                "nit": "NIT135791357",
                "id_proveedor": 7
            },
            {
                "no_factura": "FAC008",
                "monto": 800.00,
                "fecha_emision": "2024-11-22 13:00:00",
                "fecha_vence": "2025-01-10 13:00:00",
                "fecha_otorga": "2024-11-22 14:00:00",
                "dias_credito": 49,
                "nombre_proveedor": "DigitalGenio Tech",
                "nit": "NIT246802468",
                "id_proveedor": 5
            },
            {
                "no_factura": "FAC009",
                "monto": 2500.00,
                "fecha_emision": "2024-11-25 10:00:00",
                "fecha_vence": "2025-02-05 10:00:00",
                "fecha_otorga": "2024-11-25 11:00:00",
                "dias_credito": 72,
                "nombre_proveedor": "FutureTech Innovators",
                "nit": "NIT987654321",
                "id_proveedor": 3
            },
            {
                "no_factura": "FAC010",
                "monto": 6000.00,
                "fecha_emision": "2024-11-28 16:00:00",
                "fecha_vence": "2025-03-15 16:00:00",
                "fecha_otorga": "2024-11-28 17:00:00",
                "dias_credito": 107,
                "nombre_proveedor": "NextWave IT Solutions",
                "nit": "NIT789654321",
                "id_proveedor": 5
            }
        ]

        for factura_data in facturas:
            factura = Factura.query.filter_by(no_factura=factura_data["no_factura"]).first()
            if not factura:
                factura = Factura(**factura_data)
                db.session.add(factura)
        db.session.commit()
        print("Seeds para 'facturas' creados exitosamente.")

@seed_cli.command('all')
def seed_all():
    """Ejecuta todos los comandos de seeds"""
    print("Iniciando el seed de todas las tablas...")
    with current_app.app_context():
        try:
            seed_parametros()
            seed_estados()
            seed_roles()
            seed_proveedores()
            seed_facturas()
            print("Seeds ejecutados correctamente en todas las tablas.")
        except Exception as e:
            print(f"Error al ejecutar seeds: {e}")

def init_app(app):
    app.cli.add_command(seed_cli)
