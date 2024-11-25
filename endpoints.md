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
### **Cerrar Sesión**
**Endpoint:** `POST /api/usuario/cerrar-sesion?usuario_id=1`  
**Descripción:** Cierra la session del usuario.

**Headers:**
```json
{
    "Authorization": "Bearer <access_token>"
}
```

**Response:**
```json

{
    "data":null,
    "message": "Se ha cerrado la session exitosamente",
    "code": 0
}

```


## Endpoints Solicitudes

### **Listar todas las solicitudes**
**Endpoint:** `GET /api/solicitud/obtener-solicitudes`
**Descripción:** Devuelve una lista de solicitudes con soporte para filtros y paginación.

**Headers:**
```json
{
    "Authorization": "Bearer <access_token>"
}
```

**Query Parameters (opcional):**
- `page`: Número de página (ejemplo: `1`).
- `per_page`: Cantidad de elementos por página (ejemplo: `10`).
- `fecha_inicio`, `fecha_fin`: Rango de fechas.
- `estado`: Filtrar por estado.
- `proveedor`: Buscar por nombre de proveedor, correo, NCR o teléfono.
- 'nombre_proveedor': nombre proveedor
- 'nrc': 
- telefono:
- correo:

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
### **Mostrar detalle de una solicitud**
**Endpoint:** `GET /api/solicitud/obtener-detalle-solicitud?id=2`
**Descripción:** Devuelve los detalles de una solicitud específica.

**Headers:**
```json
{
    "Authorization": "Bearer <access_token>"
}
```

**Response:**
```json
{
    "code": 0,
    "data": {
        "id": 1,
        "nombre_cliente": "Empresa XYZ",
        "contacto": "Juan Pérez",
        "email": "juan.perez@example.com",
        "iva": 200.0,
        "subtotal": 1000.0,
        "total": 1200.0,
        "estado": "Pendiente",
        "id_estado": 1,
        "factura": {
            "id": 5,
            "no_factura": "1234",
            "monto": 1200.0,
            "fecha_emision": "2024-11-20T00:00:00",
            "fecha_vence": "2025-01-20T00:00:00",
            "proveedor": {
                "id": 3,
                "razon_social": "Proveedor ABC",
                "correo_electronico": "proveedor@abc.com",
                "telefono": "555-1234"
            }
        }
    },
    "message": "Consulta exitosa"
}
```

### **Aprobar una solicitud**
**Endpoint:** `PUT /api/solicitud/aprobar?id=2`
**Descripción:** Cambia el estado de la solicitud a Aprobada y puede registrar información adicional sobre quién aprobó la solicitud.

**Headers:**
```json
{
    "Authorization": "Bearer <access_token>"
}
```

**Body (JSON):**
```json
{
  "id_aprobador": 5, // ID del usuario que aprueba la solicitud
  "comentario": "Documentacion satisfactoria" // (opcional) si esta definido agregarlo a la tabla de comentarios
}
```

**Response:**
```json

{
    "data":{
        "solicitud":{
            "id": 1,
            "nombre_cliente": "John Doe",
            "contacto": "12345678",
            "email": "john.doe@example.com",
            "estado": "Aprobada",
            "id_estado": 1,
            "fecha_aprobacion": "2024-11-18",
            "total": 1000.50,
            "factura": {
                    "id": 1,
                    "no_factura": "FAC123",
                    "monto": 500.00,
                    "proveedor": {
                        "id": 10,
                        "razon_social": "Proveedor S.A."
                    }
            }
        }
    },
    "message": "Solicitud aprobada exitosamente."
}

```

### **Denegar una solicitud**
**Endpoint:** `PUT /api/solicitud/denegar?id=2`
**Descripción:** Cambia el estado de la solicitud a Denegada y permite registrar una razón para la denegación.

**Headers:**
```json
{
    "Authorization": "Bearer <access_token>"
}
```

**Body (JSON):**
```json
{
  "id_aprobador": 5, // ID del usuario que deniega la solicitud
  "comentario": "Documentación incompleta." // (opcional) si esta definido agregarlo a la tabla de comentarios
}

```

**Response:**
```json

{
    "data":{
        "solicitud":{
            "id": 5,
            "nombre_cliente": "John Doe",
            "contacto": "12345678",
            "email": "john.doe@example.com",
            "estado": "Denegada",
            "id_estado": 1,
            "fecha_aprobacion": "2024-11-18",
            "total": 1000.50,
            "factura": {
                    "id": 1,
                    "no_factura": "FAC123",
                    "monto": 500.00,
                    "proveedor": {
                        "id": 10,
                        "razon_social": "Proveedor S.A."
                    }
            }
        }
    },
    "message": "Solicitud denegada."
}
```