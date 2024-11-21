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
**Endpoint:** `POST /api/factura/obtener-detalle-factura`
**Descripción:** Recibe un JSON con los datos de la factura que se desea obtener los detalles de la factura y devuelve un JSON con los resultados de la factura.

**Request Body:**
```json
{
    "cliente": "Antoni Verde",
    "id_factura": 12345,
    "fecha_otorgamiento": "20/12/2024",
    "fecha_vencimiento": "18/02/2025",
    "monto_factura": 15000
}
```

**Response:**
```json
{
    "pronto_pago": 75.0,
    "iva": 1950.0,
    "subtotal_descuento": 2025.0,
    "total_a_recibir": 12975.0,
    "cliente": "Antoni Verde",
    "id_factura": 12345,
    "dias_restantes": 60,
    "fecha_otorgamiento": "20/12/2024",
    "fecha_vencimiento": "18/02/2025",
    "monto_factura": 15000
}
```

## Endpoints Usuario

### **Crear Usuario**
**Endpoint:** `POST /api/usuario/crear-usuario`
**Descripción:** Crea un nuevo usuario en el sistema con una contraseña temporal y la almacena hasheada.

**Request Body:**
```json
{
    "nombre_completo": "Juan Pérez",
    "email": "juan.perez@example.com",
    "cargo": "Administrador",
    "id_rol": 1
}

```

**Response (success):**
```json
{
    "data": {
        "usuario_id": 1,
        "nombre_completo": "Juan Pérez",
        "email": "juan.perez@example.com",
        "cargo": "Administrador",
        "id_rol": 1
    },
    "message": "Usuario creado exitosamente",
    "code": 0
}
```
**Response (error):**
```json
{
    "data": null,
    "message": "El correo ya está registrado",
    "code": 1
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
    "data": {
        "usuario_id": 1,
        "nombre_completo": "Juan Pérez",
        "email": "juan.perez@example.com",
        "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
    },
    "message": "Inicio de sesión exitoso",
    "code": 0
}
```
**Response (error):**
```json
{
    "data": null,
    "message": "El usuario no existe",
    "code": 1
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
    "data": {
        "usuario_id": 1,
        "nombre_completo": "Juan Pérez",
        "email": "juan.perez@example.com",
        "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
    },
    "message": "Token generado exitosamente",
    "code": 0
}
```
**Response (error):**
```json
{
    "data": null,
    "message": "El campo 'email' es obligatorio",
    "code": 1
}
```