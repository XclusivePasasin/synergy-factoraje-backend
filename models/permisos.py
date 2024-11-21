from utils.db import db

class Permiso(db.Model):
    __tablename__ = 'permisos'
    id = db.Column(db.Integer, primary_key=True)
    id_rol = db.Column(db.Integer, db.ForeignKey('roles.id', ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    id_menu = db.Column(db.Integer, db.ForeignKey('menus.id', ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    create_perm = db.Column(db.Boolean, default=False)
    edit_perm = db.Column(db.Boolean, default=False)
    delete_perm = db.Column(db.Boolean, default=False)
    view_perm = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())
