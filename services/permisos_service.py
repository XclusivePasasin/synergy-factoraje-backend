from utils.db import db
from models.permisos import Permiso
from models.roles import Rol
from utils.response import response_success, response_error

class PermisosService:
    @staticmethod
    def actualizar_permisos(data):
        id_rol = data.get('id_rol')
        nombre = data.get('nombre')
        descripcion = data.get('descripcion')
        permisos = data.get('permisos')

        # Validar que los permisos estén presentes en el payload
        if not permisos:
            return response_error("No se proporcionaron permisos.", http_status=400)

        try:
            # Si el id_rol es None, se crea un nuevo rol
            if id_rol is None:
                if not nombre:
                    return response_error("El nombre del rol es obligatorio para crear un nuevo rol.", http_status=400)

                nuevo_rol = Rol(rol=nombre, nombre=nombre, descripcion=descripcion)
                db.session.add(nuevo_rol)
                db.session.commit()
                id_rol = nuevo_rol.id  # Asignar el nuevo ID del rol creado

            # Validar si el rol es predeterminado
            # if id_rol in [1, 2, 3, 4]:
            #     return response_error("No se pueden modificar los permisos para este rol.", http_status=403)

            # Validar si el rol existe
            rol = Rol.query.get(id_rol)
            if not rol:
                return response_error("ID de rol no válido.", http_status=400)

            # Eliminar permisos existentes para el rol especificado
            Permiso.query.filter_by(id_rol=id_rol).delete()
            db.session.commit()

            # Insertar nuevos permisos
            nuevos_permisos = []
            for permiso in permisos:
                nuevo_permiso = Permiso(
                    id_rol=id_rol,
                    id_menu=permiso['id_menu'],
                    create_perm=permiso.get('create_perm'),
                    edit_perm=permiso.get('edit_perm'),
                    delete_perm=permiso.get('delete_perm'),
                    view_perm=permiso.get('view_perm'),
                    approve_deny=permiso.get('approve_deny'),
                    download=permiso.get('download'),
                    process=permiso.get('process'),
                    edit_user=permiso.get('edit_user'),
                    create_user=permiso.get('create_user'),
                    active_inactive_user=permiso.get('active_inactive_user'),
                    edit_role=permiso.get('edit_role'),
                    create_role=permiso.get('create_role')
                )
                nuevos_permisos.append(nuevo_permiso)

            db.session.add_all(nuevos_permisos)
            db.session.commit()

            return response_success(f"Permisos asignados exitosamente para el rol '{rol.nombre}'.", "Permisos asignados exitosamente.")

        except Exception as e:
            db.session.rollback()
            return response_error(f"Ocurrió un error: {str(e)}", http_status=500)


    @staticmethod
    def obtener_permisos_por_rol(id_rol):
        # Validar si el rol existe
        rol = Rol.query.get(id_rol)
        if not rol:
            return response_error("ID de rol no válido.", http_status=400)

      # Obtener todos los permisos asociados a ese rol
        permisos = Permiso.query.filter_by(id_rol=id_rol).all()

        # Lista de nombres de los campos de permisos a incluir
        campos_permisos = [
            "create_perm", "edit_perm", "delete_perm", "view_perm",
            "approve_deny", "download", "process",
            "edit_user", "create_user", "active_inactive_user",
            "edit_role", "create_role"
        ]

        # Construir la lista de permisos filtrando dinámicamente los campos no nulos y convirtiendo a 1 o 0
        permisos_list = [
            {
                "id_menu": permiso.id_menu,
                **{campo: 1 if getattr(permiso, campo) else 0 for campo in campos_permisos if getattr(permiso, campo) is not None}
            }
            for permiso in permisos
        ]
        # Construir el payload de respuesta
        response_data = {
            "id_rol": rol.id,
            "nombre": rol.nombre,
            "descripcion": rol.descripcion,
            "permisos": permisos_list
        }

        return response_success(response_data, "Permisos obtenidos exitosamente.")