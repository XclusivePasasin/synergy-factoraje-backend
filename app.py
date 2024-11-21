from flask import Flask
from flask_migrate import Migrate
from utils.db import db
# Modelos
from models.usuarios import Usuario
from models.facturas import Factura
from models.roles import Rol
from models.estados import Estado
from models.solicitudes import Solicitud
from models.proveedores_calificados import ProveedorCalificado
from models.comentarios import Comentario
from models.bitacoras import Bitacora
from models.permisos import Permiso
from models.menus import Menu
from models.parametros import Parametro
from models.desembolsos import Desembolso
# Rutas
from routes.envio_correo import email_bp  
from routes.facturas_route import facturas_bp
from routes.usuario_route import usuarios_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)
    Migrate(app, db)  

    app.register_blueprint(email_bp, url_prefix='/api/email')
    app.register_blueprint(facturas_bp, url_prefix='/api/factura')
    app.register_blueprint(usuarios_bp, url_prefix='/api/usuario')

    return app

if __name__ == '__main__':
    app = create_app()  
    print(app.url_map)
    app.run(debug=True)
