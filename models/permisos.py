from utils.db import db

class Permiso(db.Model):
    __tablename__ = 'permisos'
    id = db.Column(db.Integer, primary_key=True)
    id_rol = db.Column(db.Integer, db.ForeignKey('roles.id', ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    id_menu = db.Column(db.Integer, db.ForeignKey('menus.id', ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    create_perm = db.Column(db.Boolean,  nullable=True)
    edit_perm = db.Column(db.Boolean,  nullable=True)
    delete_perm = db.Column(db.Boolean,  nullable=True)
    view_perm = db.Column(db.Boolean,  nullable=True)
    approve_deny = db.Column(db.Boolean,  nullable=True)
    download = db.Column(db.Boolean,  nullable=True)
    process = db.Column(db.Boolean,  nullable=True)
    edit_user = db.Column(db.Boolean,  nullable=True)
    create_user = db.Column(db.Boolean,  nullable=True)
    active_inactive_user = db.Column(db.Boolean,  nullable=True)
    edit_role = db.Column(db.Boolean,  nullable=True)
    create_role = db.Column(db.Boolean,  nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())
