from utils.db import db
from models.permisos import Permiso
from models.roles import Rol
from utils.response import response_success, response_error

class PermisosService:
    @staticmethod
    def actualizar_permisos(data):
        id_rol = data.get('id_rol')
        permisos = data.get('permisos')

        # Validar si el rol es de administrador
        if id_rol == 1:
            return response_error("No se pueden modificar los permisos del rol de Administrador.", http_status=403)

        # Validar si el rol existe
        rol = Rol.query.get(id_rol)
        if not rol:
            return response_error("ID de rol no válido.", http_status=400)

        try:
            # Eliminar permisos existentes para el rol especificado
            Permiso.query.filter_by(id_rol=id_rol).delete()
            db.session.commit()

            # Insertar nuevos permisos
            nuevos_permisos = []
            for permiso in permisos:
                nuevo_permiso = Permiso(
                    id_rol=id_rol,
                    id_menu=permiso['id_menu'],
                    create_perm=bool(permiso.get('create_perm', 0)),
                    edit_perm=bool(permiso.get('edit_perm', 0)),
                    delete_perm=bool(permiso.get('delete_perm', 0)),
                    view_perm=bool(permiso.get('view_perm', 0))
                )
                nuevos_permisos.append(nuevo_permiso)

            db.session.add_all(nuevos_permisos)
            db.session.commit()

            return response_success(f"Permisos asignados exitosamente para el rol '{rol.nombre}'.", "Permisos asignados exitosamente.")

        except Exception as e:
            db.session.rollback()
            return response_error(f"Ocurrió un error: {str(e)}", http_status=500)
