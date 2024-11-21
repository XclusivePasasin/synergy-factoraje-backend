from datetime import datetime, timedelta
import hashlib
import re
from flask import current_app
import jwt
from models.usuarios import Usuario
from models.roles import Rol
from utils.db import db
from utils.response import response_success, response_error


class UsuarioService:
    @staticmethod
    def crear_usuario(data):
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
            temp_password = UsuarioService.generar_contraseña_temp()
            print('temp_password: ', temp_password)

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
    def inicio_sesion(data):
        """
        Autentica un usuario utilizando el email y genera un token JWT si las credenciales son válidas.
        """
        try:
            # Validar los campos requeridos
            if 'email' not in data or 'password' not in data:
                return response_error("Los campos 'email' y 'password' son obligatorios", http_status=400)

            email = data['email']
            password = data['password']

            # Validar formato del email
            if len(email) < 10 or len(email) > 100 or not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                return response_error("El formato o longitud del correo electrónico no es válido", http_status=400)

            # Validar longitud de la contraseña
            if len(password) < 6 or len(password) > 20:
                return response_error("La longitud de la contraseña debe estar entre 6 y 20 caracteres", http_status=400)

            # Buscar al usuario en la base de datos por email
            usuario_encontrado = Usuario.query.filter_by(email=email).first()
            if not usuario_encontrado:
                return response_error("El usuario no existe", http_status=401)

            # Generar el hash de la contraseña ingresada
            salt = current_app.config.get('SALT_SECRET')
            hashed_password = hashlib.sha256((password + salt).encode('utf-8')).hexdigest()

            # Validar la contraseña
            if hashed_password != usuario_encontrado.password:
                return response_error("La contraseña es incorrecta", http_status=401)

            # Generar el token
            token_data = UsuarioService.crear_token(email)  # Usar email

            if not token_data:
                return response_error("Error al generar el token", http_status=500)

            # Responder con los datos del usuario y el token
            respuesta = {
                "usuario_id": token_data["usuario_id"],
                "nombre_completo": token_data["nombre_completo"],
                "email": token_data["email"],
                "token": token_data["token"]
            }
            return response_success(respuesta, "Inicio de sesión exitoso", http_status=200)
        except Exception as e:
            return response_error(f"Error interno del servidor: {str(e)}", http_status=500)
    
    @staticmethod
    def generar_contraseña_temp(length=10):
        import string
        import random
        caracteres = string.ascii_letters + string.digits
        return ''.join(random.choice(caracteres) for _ in range(length))

    @staticmethod
    def crear_token(email):
        """
        Crea un token JWT con una validez de 24 horas y lo guarda en el usuario.
        """
        try:
            # Obtener clave secreta desde configuración
            secret_key = current_app.config.get('SECRET_KEY')
            expiration = datetime.utcnow() + timedelta(hours=24)

            payload = {
                'email': email,  
                'exp': expiration
            }

            # Generar el token JWT
            token = jwt.encode(payload, secret_key, algorithm='HS256')

            # Actualizar el token en la base de datos
            usuario_encontrado = Usuario.query.filter_by(email=email).first()  
            if not usuario_encontrado:
                return None  

            usuario_encontrado.token = token
            usuario_encontrado.token_date_end = expiration

            db.session.commit()

            return {
                "usuario_id": usuario_encontrado.id,
                "nombre_completo": usuario_encontrado.nombre_completo,
                "email": usuario_encontrado.email,
                "token": token
            }
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Error al crear el token: {str(e)}")
    
    @staticmethod
    def cargar_token(data):
        """
        Genera un nuevo token para un usuario existente basado en su email.
        """
        try:
            # Validar que se haya proporcionado el email
            if 'email' not in data:
                return response_error("El campo 'email' es obligatorio", http_status=400)

            email = data['email']

            # Validar longitud y formato del email
            if len(email) < 10 or len(email) > 100 or not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                return response_error("El formato o longitud del correo electrónico no es válido", http_status=400)

            # Buscar al usuario en la base de datos por email
            usuario_encontrado = Usuario.query.filter_by(email=email).first()
            if not usuario_encontrado:
                return response_error("El usuario no existe", http_status=404)

            # Generar un nuevo token
            token_data = UsuarioService.crear_token(email)

            if not token_data:
                return response_error("Error al generar el token", http_status=500)

            # Retornar los datos del usuario y el nuevo token
            respuesta = {
                "usuario_id": token_data["usuario_id"],
                "nombre_completo": token_data["nombre_completo"],
                "email": token_data["email"],
                "token": token_data["token"]
            }
            return response_success(respuesta, "Token generado exitosamente", http_status=200)
        except Exception as e:
            return response_error(f"Error interno del servidor: {str(e)}", http_status=500)

        
    @staticmethod
    def validar_token(token):
        """
        Valida la vigencia del token JWT.
        :param token: El token de sesión.
        :return: 'valido' si el token es válido, 'vencido' si ha expirado, 'invalido' si es inválido.
        """
        try:
            # Obtener la clave secreta desde la configuración
            secret_key = current_app.config.get('SECRET_KEY')
            # Decodificar el token JWT
            jwt.decode(token, secret_key, algorithms=['HS256'])
            # Si no se lanza una excepción, el token es válido
            return 'valido'
        except jwt.ExpiredSignatureError:
            # El token ha expirado
            return 'vencido'
        except jwt.InvalidTokenError:
            # El token es inválido
            return 'invalido'

