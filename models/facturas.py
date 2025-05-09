from utils.db import db

class Factura(db.Model):
    __tablename__ = 'facturas'
    id = db.Column(db.Integer, primary_key=True)
    no_factura = db.Column(db.String(50), nullable=False)
    monto = db.Column(db.Numeric(10, 2), nullable=False)
    fecha_emision = db.Column(db.DateTime, nullable=False)
    fecha_vence = db.Column(db.DateTime, nullable=False)
    fecha_otorga = db.Column(db.DateTime, nullable=False)
    dias_credito = db.Column(db.Integer, nullable=False)
    nombre_proveedor = db.Column(db.String(255))
    nit = db.Column(db.String(50))
    id_proveedor = db.Column(db.Integer, db.ForeignKey('proveedores_calificados.id', ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    proveedor = db.relationship('ProveedorCalificado', backref='facturas')
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())
