import hashlib
import re
from flask import current_app
from models.usuarios import Usuario
from models.roles import Rol
from utils.db import db
from utils.response import response_success, response_error


class UsuarioService:
    @staticmethod
    def create_user(data):
        try:
            # Validar los campos requeridos
            campos_requeridos = ['nombre_completo', 'email', 'cargo', 'id_rol']
            for campo in campos_requeridos:
                if campo not in data:
                    return response_error(f"El campo {campo} es obligatorio", http_status=400)

            nombre_completo = data['nombre_completo']
            email = data['email']
            cargo = data['cargo']
            id_rol = data['id_rol']

            # Validar longitud y formato del correo electrónico
            if len(email) < 10 or len(email) > 100 or not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                return response_error("El formato o longitud del correo electrónico no es válido", http_status=400)

            # Validar que el rol existe
            rol = Rol.query.get(id_rol)
            if not rol:
                return response_error("El rol especificado no existe", http_status=404)

            # Validar que el correo no esté registrado
            usuario_existente = Usuario.query.filter_by(email=email).first()
            if usuario_existente:
                return response_error("El correo ya está registrado", http_status=409)

            # Generar contraseña temporal
            temp_password = UsuarioService.generate_temp_password()

            # Hashear la contraseña y la contraseña temporal usando hashlib con SHA-256
            salt = current_app.config['SALT_SECRET'] 
            hashed_password = hashlib.sha256((temp_password + salt).encode('utf-8')).hexdigest()
            hashed_temp_password = hashlib.sha256((temp_password + salt).encode('utf-8')).hexdigest()

            # Crear el nuevo usuario
            nuevo_usuario = Usuario(
                nombre_completo=nombre_completo,
                email=email,
                password=hashed_password,
                temp_password=hashed_temp_password,
                cargo=cargo,
                id_rol=id_rol
            )

            # Guardar en la base de datos
            db.session.add(nuevo_usuario)
            db.session.commit()

            # Retornar detalles del usuario creado (sin incluir contraseñas)
            respuesta = {
                "usuario_id": nuevo_usuario.id,
                "nombre_completo": nuevo_usuario.nombre_completo,
                "email": nuevo_usuario.email,
                "cargo": nuevo_usuario.cargo,
                "id_rol": nuevo_usuario.id_rol
            }
            return response_success(respuesta, "Usuario creado exitosamente", http_status=201)
        except Exception as e:
            # Revertir cambios en caso de error
            db.session.rollback()
            return response_error(f"Error interno del servidor: {str(e)}", http_status=500)

    @staticmethod
    def generate_temp_password(length=10):
        import string
        import random
        caracteres = string.ascii_letters + string.digits
        return ''.join(random.choice(caracteres) for _ in range(length))
