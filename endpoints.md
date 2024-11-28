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
        "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InRlc3RAYWRtaW4uY29tIiwiZXhwIjoxNzMyODIwMzY2fQ.11UCiRhAEGG_9gxEsjyVA5LLQ-5fqL2_pmEJeh5GoII",
        "expires_in": 86400,
        "usuario": {
            "email": "test@admin.com",
            "id": 2,
            "name": "Test",
            "permissions": [
                {
                    "create_perm": 1,
                    "delete_perm": 0,
                    "edit_perm": 1,
                    "menu": {
                        "icon": "fa-solid-file",
                        "id": 1,
                        "menu": "Solicitudes",
                        "orden": 2,
                        "padre": 0,
                        "path": "/solicitudes"
                    },
                    "view_perm": 0
                }
            ],
            "role": "Administrador"
        }
    },
    "message": "Autenticación completada"
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
        "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InRlc3RAYWRtaW4uY29tIiwiZXhwIjoxNzMyODIwMzY2fQ.11UCiRhAEGG_9gxEsjyVA5LLQ-5fqL2_pmEJeh5GoII",
        "expires_in": 86400,
        "usuario": {
            "email": "test@admin.com",
            "id": 2,
            "name": "Test",
            "permissions": [
                {
                    "create_perm": 1,
                    "delete_perm": 0,
                    "edit_perm": 1,
                    "menu": {
                        "icon": "fa-solid-file",
                        "id": 1,
                        "menu": "Solicitudes",
                        "orden": 2,
                        "padre": 0,
                        "path": "/solicitudes"
                    },
                    "view_perm": 0
                }
            ],
            "role": "Administrador"
        }
    },
    "message": "Autenticación completada"
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
- 'page': Número de página (ejemplo: `1`).
- 'per_page': Cantidad de elementos por página (ejemplo: `10`).
- 'fecha_inicio', `fecha_fin`: Rango de fechas.
- 'estado': Filtrar por estado.
- 'no_factura': Filtrar por número de factura.
- 'nombre_proveedor': nombre proveedor
- 'nrc': 
- 'telefono':
- 'correo':

**Response (success):**
```json
{
    "code": 0,
    "data": {
        "current_page": 1,
        "per_page": 10,
        "solicitudes": [
            {
                "contacto": "555-67891",
                "email": "misael.gutierrez@clobi.cl",
                "estado": "PENDIENTE",
                "factura": {
                    "fecha_emision": "2024-11-05T09:00:00",
                    "fecha_otorga": "2024-11-05T09:30:00",
                    "fecha_vence": "2025-01-19T09:00:00",
                    "id": 2,
                    "monto": 3000.0,
                    "no_factura": "FAC002",
                    "proveedor": {
                        "correo_electronico": "info@futuretech.com",
                        "id": 2,
                        "max_factoring": "8000.00",
                        "min_factoring": "2000.00",
                        "nit": "NIT987654321",
                        "nombre_contacto": "Sofía Ramírez",
                        "nrc": "NRC67891",
                        "razon_social": "FutureTech Innovators",
                        "telefono": "555-67891"
                    }
                },
                "id": 4,
                "id_estado": 1,
                "iva": 10.72,
                "nombre_cliente": "Misael Gutierrez",
                "subtotal": 93.22,
                "total": 2906.78
            }
        ],
        "total_pages": 1
    },
    "message": "Consulta exitosa"
}
```
### **Mostrar detalle de una solicitud**
**Endpoint:** `GET /api/solicitud/obtener-detalle-solicitud?id=`
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
        "contacto": "555-67891",
        "email": "misael.gutierrez@clobi.cl",
        "estado": "PENDIENTE",
        "factura": {
            "fecha_emision": "2024-11-05T09:00:00",
            "fecha_vence": "2025-01-19T09:00:00",
            "id": 2,
            "monto": 3000.0,
            "no_factura": "FAC002",
            "proveedor": {
                "correo_electronico": "info@futuretech.com",
                "id": 2,
                "razon_social": "FutureTech Innovators",
                "telefono": "555-67891"
            }
        },
        "id": 4,
        "id_estado": 1,
        "iva": 10.72,
        "nombre_cliente": "Misael Gutierrez",
        "subtotal": 93.22,
        "total": 2906.78
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