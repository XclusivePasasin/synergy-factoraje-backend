# Documentación de API - Endpoints del backend

## Endpoints Email

### **Enviar correo electrónico de factura**
**Endpoint:** `POST /api/email/enviar-email`
**Descripción:** Envia un correo electrónico con los datos de la solicitud de factura.

**Request Body:**
```json
{
    "destinatario": "example@gmail.com",
    "asunto": "Opción de Pronto Pago Disponible",
    "datos": {
        "nombreEmpresa": "Clobi Technologies S.A. de C.V.",
        "noFactura": "11111",
        "monto": "10000.00",
        "fechaOtorgamiento": "20/11/2024",
        "fechaVencimiento": "19/02/2025",
        "diasCredito": "91",
        "linkBoton": "https://ejemplo.com/pronto-pago"
    }
}

```

## Endpoint Solicitud de Pago

### **Obtener detalles pronto pago de la factura**
**Endpoint:** `GET /api/factura/obtener-detalle-factura?no_factura=555`
**Descripción:** Recibe un JSON con los datos de la factura que se desea obtener los detalles de la factura y devuelve un JSON con los resultados de la factura.

**Request Body:**
```json

```

**Response:**
```json
{
    "code": 0,
    "data": {
        "factura": {
            "cliente": "Clobi Technologies S.A. de C.V.",
            "dias_restantes": 87,
            "fecha_otorgamiento": "20/11/2024",
            "fecha_vencimiento": "18/02/2025",
            "iva": 84.83,
            "monto_factura": 15000.0,
            "no_factura": "555",
            "pronto_pago": 652.5,
            "subtotal_descuento": 737.33,
            "total_a_recibir": 14262.67
        }
    },
    "message": "Detalle de factura obtenido correctamente"
}
```

## Endpoints Usuario

### **Crear Usuario**
**Endpoint:** `POST /api/usuario/crear-usuario`
**Descripción:** Crea un nuevo usuario en el sistema con una contraseña temporal y la almacena hasheada.

**Request Body:**
```json
{
    "nombre_completo": "Julian Zan",
    "email": "julian.zan4@example.com",
    "cargo": "Gerente",
    "id_rol": 1
}

```

**Response (success):**
```json
{
    "code": 0,
    "data": {
        "cargo": "Gerente",
        "email": "julian.zan5@example.com",
        "id_rol": 1,
        "nombre_completo": "Julian Zan",
        "usuario_id": 5
    },
    "message": "Usuario creado exitosamente"
}
```
**Response (error):**
```json
{
    "code": 1,
    "data": null,
    "message": "El correo ya está registrado"
}
```

### **Iniciar Sesión**

**Endpoint:** `POST /api/usuario/inicio-sesion`
**Descripción:** Inicia sesión en el sistema con el email y la contraseña proporcionados y genera un token JWT.

**Request Body:**
```json
{
    "email": "juan.perez@example.com",
    "password": "12345678"
}
```

**Response (success):**
```json
{
    "code": 0,
    "data": {
        "email": "julian.zan3@example.com",
        "nombre_completo": "Julian Zan",
        "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6Imp1bGlhbi56YW4zQGV4YW1wb...",
        "usuario_id": 3
    },
    "message": "Inicio de sesión exitoso"
}
```
**Response (error):**
```json
{
    "code": 1,
    "data": null,
    "message": "El usuario no existe"
}
```

### **Validar Token**

**Endpoint:** `POST /api/usuario/token`
**Descripción:** Valida el token JWT proporcionado y devuelve el usuario y el token.

**Request Body:**
```json
{
    "email": "email@ejemplo.com",
}


```

**Response (success):**
```json
{
    "code": 0,
    "data": {
        "email": "julian.zan3@example.com",
        "nombre_completo": "Julian Zan",
        "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9....",
        "usuario_id": 3
    },
    "message": "Token generado exitosamente"
}
```
**Response (error):**
```json
{
    "code": 1,
    "data": null,
    "message": "El usuario no existe"
}
```