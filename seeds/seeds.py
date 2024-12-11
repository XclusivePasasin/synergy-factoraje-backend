from flask.cli import AppGroup
from flask import current_app
from extensions import db
from models.parametros import Parametro
from models.estados import Estado
from models.proveedores_calificados import ProveedorCalificado
from models.facturas import Factura
from models.menus import Menu
from models.permisos import Permiso
from models.roles import Rol

# Crear un grupo de comandos para seeds
seed_cli = AppGroup('seed')

@seed_cli.command('parametros')
def seed_parametros():
    """Seed de parámetros"""
    with current_app.app_context():
        parametros = [
            {"clave": "INT_AN_PP", "valor": "18"},
            {"clave": "NOM-EMPRESA", "valor": "Synergy Financial Corp"},
            {"clave": "ENC-EMPRESA", "valor": "Vanessa Chicas"},
            {"clave": "TEL-EMPRESA", "valor": "7777-5578"},
            {"clave": "MAIL-EMPRESA", "valor": "eliazar.rebollo23@gmail.com"}
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
                "clave": "PENDIENTE",
                "descripcion": "Estado que indica que el desembolso esta pendiente de procesar por el agente de Synergy",
                "clasificacion": "Desembolso"
            },
            {
                "clave": "DESEMBOLSADA",
                "descripcion": "Estado que indica que el desembolso se ha procesado en una transacción bancaria",
                "clasificacion": "Desembolso"
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
            },
            {
                "rol": "Operador de ICC",
                "nombre": "Operador de ICC",
                "descripcion": None
            },
            {
                "rol": "Operador de Synergy",
                "nombre": "Operador de Synergy",
                "descripcion": None
            },
            {
                "rol": "Auditor",
                "nombre": "Auditor",
                "descripcion": None
            },
            {
                "rol": "Solicitador",
                "nombre": "Solicitante de Pronto Pago",
                "descripcion": None
            },
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
                "razon_social": "Clobi Technologies S.A. de C.V.",
                "nrc": "NRC12345",
                "nit": "NIT456789123",
                "min_factoring": 1000.00,
                "max_factoring": 5000.00,
                "cuenta_bancaria": "1234567890",
                "nombre_contacto": "Juan Pérez",
                "correo_electronico": "clobitech@clobitech.com",
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
                "no_factura": "DTE-03M001P001-000000000000580",
                "monto": 1806.87,
                "fecha_emision": "2024-11-30 00:00:00",
                "fecha_vence": "2025-01-30 00:00:00",  
                "fecha_otorga": "2024-11-30 01:00:00",  
                "dias_credito": 60,
                "nombre_proveedor": "2V TRADING EL SALVADOR, S.A. DE C.V",
                "nit": "0614-271014-103-8",
                "noti_cliente": "N",
                "noti_contador": "N",
                "factura_hash": "hash_pl0001_580",
                "id_proveedor": 1
            },
            {
                "no_factura": "DTE-03-M001P001-0000000000000536",
                "monto": 2529.62,
                "fecha_emision": "2024-11-12 00:00:00",
                "fecha_vence": "2025-01-12 00:00:00",  
                "fecha_otorga": "2024-11-12 01:00:00",  
                "dias_credito": 61,
                "nombre_proveedor": "2V TRADING EL SALVADOR, S.A. DE C.V",
                "nit": "0614-271014-103-8",
                "noti_cliente": "N",
                "noti_contador": "N",
                "factura_hash": "hash_pl0001_536",
                "id_proveedor": 1
            },
            {
                "no_factura": "DTE-03-S002P001-240000000000872",
                "monto": 7573.80,
                "fecha_emision": "2024-11-30 00:00:00",
                "fecha_vence": "2025-01-30 00:00:00",  
                "fecha_otorga": "2024-11-30 01:00:00",  
                "dias_credito": 60,
                "nombre_proveedor": "2V TRADING EL SALVADOR, S.A. DE C.V",
                "nit": "0614-271014-103-8",
                "noti_cliente": "N",
                "noti_contador": "N",
                "factura_hash": "hash_pl0001_872",
                "id_proveedor": 1
            },
            {
                "no_factura": "DTE-03-M001P001-000000000000579",
                "monto": 2529.62,
                "fecha_emision": "2024-11-30 00:00:00",
                "fecha_vence": "2025-01-30 00:00:00",  
                "fecha_otorga": "2024-11-30 01:00:00",  
                "dias_credito": 11,
                "nombre_proveedor": "2V TRADING EL SALVADOR, S.A. DE C.V",
                "nit": "0614-271014-103-8",
                "noti_cliente": "N",
                "noti_contador": "N",
                "factura_hash": "hash_pl0001_579",
                "id_proveedor": 1
            },
            {
                "no_factura": "DTE-03-M001P001-000000000002607",
                "monto": 1345.49,
                "fecha_emision": "2024-10-30 00:00:00",
                "fecha_vence": "2024-12-30 00:00:00", 
                "fecha_otorga": "2024-10-30 01:00:00",  
                "dias_credito": 60,
                "nombre_proveedor": "BRENNTAG EL SALVADOR, S.A. DE C.V.",
                "nit": "0614-150277-002-9",
                "noti_cliente": "N",
                "noti_contador": "N",
                "factura_hash": "hash_pl0003_2607",
                "id_proveedor": 2
            }
        ]

        for factura_data in facturas:
            factura = Factura.query.filter_by(no_factura=factura_data["no_factura"]).first()
            if not factura:
                factura = Factura(**factura_data)
                db.session.add(factura)

        db.session.commit()
        print("Seeds para 'facturas' creados exitosamente.")

        
        
from models.usuarios import Usuario
from utils.db import db

@seed_cli.command('menus')
def seed_menus():
    """Seed de menus"""
    with current_app.app_context():
        menus = [
            {
                "id": 1,
                "menu": "Panel",
                "description": "Este menu muestra la informacion como acceso directo",
                "path": "/home",
                "icon": "pi pi-chart-line",
                "padre": 0,
                "orden": 1,
            },
            {
                "id": 2,
                "menu": "Solicitudes",
                "description": "Este menu muestra las solicitudes que estan pendientes",
                "path": "/solicitudes",
                "icon": "pi pi-chart-bar",
                "padre": 0,
                "orden": 2,
            },
            {
                "id": 3,
                "menu": "Aprobadas",
                "description": None,
                "path": "/solicitudes/aprobadas",
                "icon": "pi pi-check-circle",
                "padre": 2,
                "orden": 2,
            },
            {
                "id": 4,
                "menu": "Sin Aprobar",
                "description": None,
                "path": "/solicitudes/sin-aprobar",
                "icon": "pi pi-hourglass",
                "padre": 2,
                "orden": 2,
            },
            {
                "id": 5,
                "menu": "Desembolso",
                "description": None,
                "path": "/desembolsos",
                "icon": "pi pi-shopping-bag",
                "padre": 0,
                "orden": 3,
            },
            {
                "id": 6,
                "menu": "Procesadas",
                "description": None,
                "path": "/desembolsos/procesadas",
                "icon": "pi-chart-bar",
                "padre": 3,
                "orden": 3,
            },
            {
                "id": 7,
                "menu": "Ajustes",
                "description": None,
                "path": "/ajustes",
                "icon": "pi pi-sliders-h",
                "padre": 0,
                "orden": 4,
            },
            {
                "id": 8,
                "menu": "Administracion",
                "description": None,
                "path": "/administracion",
                "icon": "pi pi-users",
                "padre": 0,
                "orden": 5,
            },
            {
                "id": 9,
                "menu": "Reportes",
                "description": None,
                "path": "/reportes",
                "icon": "pi pi-warehouse",
                "padre": 0,
                "orden": 6,
            },
            {
                "id": 10,
                "menu": "Bitacoras",
                "description": None,
                "path": "/reportes/bitacoras",
                "icon": "pi-chart-bar",
                "padre": 6,
                "orden": 6.1,
            },
            {
                "id": 11,
                "menu": "Solicitar Pronto Pago",
                "description": None,
                "path": "/solicitar-pronto-pago",
                "icon": "pi-chart-bar",
                "padre": 0,
                "orden": 7,
            },
            {
                "id": 12,
                "menu": "Usuarios",
                "description": None,
                "path": "/admin/usuarios",
                "icon": "pi pi-users",
                "padre": 8,
                "orden": 5.1,
            },
            {
                "id": 13,
                "menu": "Roles y permisos",
                "description": None,
                "path": "/admin/roles-permisos",
                "icon": "pi pi-shield",
                "padre": 8,
                "orden": 5.2,
            },
        ]

        for menu in menus:
            new_menu = Menu(
                id=menu["id"],
                menu=menu["menu"],
                description=menu["description"],
                path=menu["path"],
                icon=menu["icon"],
                orden=menu["orden"],
                padre=menu["padre"],
            )
            db.session.add(new_menu)
        
        db.session.commit()
        print("Menús insertados exitosamente.")
        
@seed_cli.command('permisos')
def seed_permisos():
    """Seed de permisos"""
    with current_app.app_context():
        permisos = [
            {"id": 1, "id_rol": 1, "id_menu": 1, "create_perm": True, "edit_perm": True, "delete_perm": True, "view_perm": True, "approve_deny": True, "download": True, "process": True, "edit_user": True, "create_user": True, "active_inactive_user": True, "edit_role": True, "create_role": True},
            {"id": 2, "id_rol": 1, "id_menu": 2, "create_perm": True, "edit_perm": True, "delete_perm": True, "view_perm": True, "approve_deny": True, "download": True, "process": True, "edit_user": True, "create_user": True, "active_inactive_user": True, "edit_role": True, "create_role": True},
            {"id": 3, "id_rol": 1, "id_menu": 3, "create_perm": True, "edit_perm": True, "delete_perm": True, "view_perm": True, "approve_deny": True, "download": True, "process": True, "edit_user": True, "create_user": True, "active_inactive_user": True, "edit_role": True, "create_role": True},
            {"id": 4, "id_rol": 1, "id_menu": 4, "create_perm": True, "edit_perm": True, "delete_perm": True, "view_perm": True, "approve_deny": True, "download": True, "process": True, "edit_user": True, "create_user": True, "active_inactive_user": True, "edit_role": True, "create_role": True},
            {"id": 5, "id_rol": 1, "id_menu": 5, "create_perm": True, "edit_perm": True, "delete_perm": True, "view_perm": True, "approve_deny": True, "download": True, "process": True, "edit_user": True, "create_user": True, "active_inactive_user": True, "edit_role": True, "create_role": True},
            {"id": 6, "id_rol": 1, "id_menu": 6, "create_perm": True, "edit_perm": True, "delete_perm": True, "view_perm": True, "approve_deny": True, "download": True, "process": True, "edit_user": True, "create_user": True, "active_inactive_user": True, "edit_role": True, "create_role": True},
            {"id": 7, "id_rol": 1, "id_menu": 7, "create_perm": True, "edit_perm": True, "delete_perm": True, "view_perm": True, "approve_deny": True, "download": True, "process": True, "edit_user": True, "create_user": True, "active_inactive_user": True, "edit_role": True, "create_role": True},
            {"id": 8, "id_rol": 1, "id_menu": 8, "create_perm": True, "edit_perm": True, "delete_perm": True, "view_perm": True, "approve_deny": True, "download": True, "process": True, "edit_user": True, "create_user": True, "active_inactive_user": True, "edit_role": True, "create_role": True},
            {"id": 9, "id_rol": 1, "id_menu": 9, "create_perm": True, "edit_perm": True, "delete_perm": True, "view_perm": True, "approve_deny": True, "download": True, "process": True, "edit_user": True, "create_user": True, "active_inactive_user": True, "edit_role": True, "create_role": True},
            {"id": 10, "id_rol": 1, "id_menu": 10, "create_perm": True, "edit_perm": True, "delete_perm": True, "view_perm": True, "approve_deny": True, "download": True, "process": True, "edit_user": True, "create_user": True, "active_inactive_user": True, "edit_role": True, "create_role": True},

            {"id": 11, "id_rol": 2, "id_menu": 1, "create_perm": True, "edit_perm": True, "delete_perm": True, "view_perm": True, "approve_deny": False, "download": False, "process": False, "edit_user": False, "create_user": False, "active_inactive_user": False, "edit_role": False, "create_role": False},
            {"id": 12, "id_rol": 2, "id_menu": 2, "create_perm": True, "edit_perm": True, "delete_perm": True, "view_perm": True, "approve_deny": False, "download": False, "process": False, "edit_user": False, "create_user": False, "active_inactive_user": False, "edit_role": False, "create_role": False},
            {"id": 13, "id_rol": 2, "id_menu": 3, "create_perm": True, "edit_perm": True, "delete_perm": True, "view_perm": True, "approve_deny": False, "download": False, "process": False, "edit_user": False, "create_user": False, "active_inactive_user": False, "edit_role": False, "create_role": False},
            {"id": 14, "id_rol": 2, "id_menu": 4, "create_perm": True, "edit_perm": True, "delete_perm": True, "view_perm": True, "approve_deny": False, "download": False, "process": False, "edit_user": False, "create_user": False, "active_inactive_user": False, "edit_role": False, "create_role": False},
            {"id": 15, "id_rol": 2, "id_menu": 5, "create_perm": True, "edit_perm": True, "delete_perm": True, "view_perm": True, "approve_deny": False, "download": False, "process": False, "edit_user": False, "create_user": False, "active_inactive_user": False, "edit_role": False, "create_role": False},
            {"id": 16, "id_rol": 2, "id_menu": 6, "create_perm": True, "edit_perm": True, "delete_perm": True, "view_perm": True, "approve_deny": False, "download": False, "process": False, "edit_user": False, "create_user": False, "active_inactive_user": False, "edit_role": False, "create_role": False},
            

            {"id": 17, "id_rol": 3, "id_menu": 1, "create_perm": True, "edit_perm": True, "delete_perm": True, "view_perm": True, "approve_deny": False, "download": False, "process": False, "edit_user": False, "create_user": False, "active_inactive_user": False, "edit_role": False, "create_role": False},
            {"id": 18, "id_rol": 3, "id_menu": 9, "create_perm": True, "edit_perm": True, "delete_perm": True, "view_perm": True, "approve_deny": False, "download": False, "process": False, "edit_user": False, "create_user": False, "active_inactive_user": False, "edit_role": False, "create_role": False},
            {"id": 19, "id_rol": 3, "id_menu": 10, "create_perm": True, "edit_perm": True, "delete_perm": True, "view_perm": True, "approve_deny": False, "download": False, "process": False, "edit_user": False, "create_user": False, "active_inactive_user": False, "edit_role": False, "create_role": False},

            {"id": 20, "id_rol": 4, "id_menu": 11, "create_perm": True, "edit_perm": True, "delete_perm": True, "view_perm": True, "approve_deny": False, "download": False, "process": False, "edit_user": False, "create_user": False, "active_inactive_user": False, "edit_role": False, "create_role": False}
        ]


        for permiso in permisos:
            new_permiso = Permiso(
                id=permiso["id"],
                id_rol=permiso["id_rol"],
                id_menu=permiso["id_menu"],
                create_perm=permiso["create_perm"],
                edit_perm=permiso["edit_perm"],
                delete_perm=permiso["delete_perm"],
                view_perm=permiso["view_perm"]
            )
            db.session.add(new_permiso)

        db.session.commit()
        print("Permisos insertados exitosamente.")


@seed_cli.command('usuarios')
def seed_usuarios():
    """Seed de usuarios"""
    with current_app.app_context():
        usuarios = [
            {
                "id": 1,
                "nombres": "Administrador",
                "apellidos": "Clobi Technologies",
                "email": "clobitechadmin@clobitech.com",
                "password": None,
                "temp_password": "9c067f586228cecb9c8bc50de2b33eeb7a2c2c73d406441a87977109b631207d",
                "cargo": "Administrador",
                "token": "",
                "token_date_end": None,
                "id_rol": 1,
                "activo": True,
                "reg_activo": True,
                "created_at": "2024-12-02 08:27:55",
                "updated_at": "2024-12-02 08:29:08"
            },
            {
                "id": 2,
                "nombres": "Sonia",
                "apellidos": "Navarro",
                "email": "sonia.navarro@clobitech.com",
                "password": None,
                "temp_password": "9c067f586228cecb9c8bc50de2b33eeb7a2c2c73d406441a87977109b631207d",
                "cargo": "Agente Synergy",
                "token": "",
                "token_date_end": None,
                "id_rol": 2,
                "activo": True,
                "reg_activo": True,
                "created_at": "2024-12-02 11:22:00",
                "updated_at": "2024-12-02 11:30:27"
            },
            {
                "id": 3,
                "nombres": "Antonio",
                "apellidos": "Pasasin",
                "email": "eliazar.rebollo23@gmail.com",
                "password": None,
                "temp_password": "9c067f586228cecb9c8bc50de2b33eeb7a2c2c73d406441a87977109b631207d",
                "cargo": "Auditor",
                "token": "",
                "token_date_end": None,
                "id_rol": 3,
                "activo": True,
                "reg_activo": True,
                "created_at": "2024-12-02 11:28:45",
                "updated_at": "2024-12-02 11:32:10"
            },
            {
                "id": 4,
                "nombres": "Alex",
                "apellidos": "Chinque",
                "email": "alexchinke97@gmail.com",
                "password": None,
                "temp_password": "9c067f586228cecb9c8bc50de2b33eeb7a2c2c73d406441a87977109b631207d",
                "cargo": "Proveedor",
                "token": "",
                "token_date_end": None,
                "id_rol": 4,
                "activo": True,
                "reg_activo": True,
                "created_at": "2024-12-02 11:28:45",
                "updated_at": "2024-12-02 11:32:10"
            },
        ]

        for usuario in usuarios:
            new_usuario = Usuario(
                id=usuario["id"],
                nombres=usuario["nombres"],
                apellidos=usuario["apellidos"],
                email=usuario["email"],
                password=usuario["password"],
                temp_password=usuario["temp_password"],
                cargo=usuario["cargo"],
                token=usuario["token"],
                token_date_end=usuario["token_date_end"],
                id_rol=usuario["id_rol"],
                activo=usuario["activo"],
                reg_activo=usuario["reg_activo"],
                created_at=usuario["created_at"],
                updated_at=usuario["updated_at"]
            )
            db.session.add(new_usuario)

        db.session.commit()
        print("Usuarios insertados exitosamente.")



@seed_cli.command("all")
def seed_all():
    """Ejecuta todos los comandos de seeds en el orden correcto"""
    print("Iniciando el seed de todas las tablas...")
    with current_app.app_context():
        try:
            seed_parametros()
            seed_estados()
            seed_roles()
            seed_menus()
            seed_proveedores()
            seed_facturas()
            seed_usuarios()
            seed_permisos()
            print("Seeds ejecutados correctamente en todas las tablas.")
        except Exception as e:
            print(f"Error al ejecutar seeds: {e}")

def init_app(app):
    app.cli.add_command(seed_cli)
