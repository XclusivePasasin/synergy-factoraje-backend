# Documentación de API - Endpoints del backend

## Endpoints Email

### **Enviar correo electrónico de factura**
**Endpoint:** `POST /api/email/enviar-email`
**Descripción:** Envia un correo electrónico con los datos de la factura para notificar al proveedor que 
su factura está disponible para aplicar a pronto pago.

**Headers:**
```json
{
    "Authorization": "Bearer <access_token>"
}
```

**Request Body:**
```json
{
    "destinatario": "test@test.com",
    "asunto": "Opción de Pronto Pago Disponible",
    "datos": {
        "nombreEmpresa": "Clobi Technologies S.A. de C.V.",
        "noFactura": "FAC001",
        "monto": "10000.00",
        "fechaOtorgamiento": "20/11/2024",
        "fechaVencimiento": "19/02/2025",
        "diasCredito": "10"
    }
}

```

## Endpoint Solicitud de Pago

### **Obtener detalles pronto pago de la factura**
**Endpoint:** `GET /api/factura/obtener-detalle-factura`
**Descripción:** Obtiene los detalles de la factura en base a los parámetros proporcionados.

**Query Parameters (Obligatorio):**
- 'no_factura': Numero de la factura que se desea obtener los detalles.

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
        "factura": {
            "descuento_pp": 33.0,
            "dias_restantes": 44,
            "fecha_otorga": "01/11/2024",
            "fecha_vence": "18/01/2025",
            "iva": 4.29,
            "monto": 1500.0,
            "no_factura": "FAC001",
            "nombre_proveedor": "TechNova Solutions S.A.",
            "subtotal": 37.29,
            "total": 1462.71
        }
    },
    "message": "Detalle de factura obtenido correctamente"
}
```

### **Solicitar Solicitud de Pronto Pago**
**Endpoint:** `POST /api/solicitud/solicitar-pago-factura`
**Descripción:** Crea una solicitud de pronto pago para la factura que se desea solicitar.

**Headers:**
```json
{
    "Authorization": "Bearer <access_token>"
}
```

**request Body:**
```json
{
   "data": {
        "factura": {
            "nombre_proveedor": "TechNova Solutions S.A.",
            "dias_restantes": 47,
            "fecha_otorga": "01/11/2024",
            "fecha_vence": "18/01/2025",
            "iva": 4.58,
            "monto": 1500.0,
            "no_factura": "FAC001",
            "descuento_app": 35.25,
            "subtotal": 39.83,
            "total": 1460.17
        },
       "nombre_solicitante": "Eliazar Antonio Rebollo Pasasin",
       "cargo": "Programador",
       "email": "eliazar.rebollo23@gmail.com"
    }
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
        "cargo": "Administrador",
        "email": "tes1t@admin.com",
        "id_rol": 1,
        "nombre_completo": "Test1",
        "usuario_id": 3
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
        "access_token": "eyJhbGciOiJIUzI1NiIsIZXADDSjfhfyn",
        "change_password": 0,
        "expires_in": 86400,
        "usuario": {
            "email": "tes1t@admin.com",
            "id": 3,
            "name": "Test1",
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

### **Actualizar Contraseña**
**Endpoint:** `POST /api/usuario/cambiar-contraseña`
**Descripción:** Actualiza la contraseña del usuario en su primera sesión.

**Headers:**
```json
{
    "Authorization": "Bearer <access_token>"
}
```

**request Body:**
```json
{
    "email": "juan.perez@example.com",
    "nueva_contrasena": "12345678"
}
```

**Response (success):**
```json
{
    "code": 0,
    "data": {
        "email": "juan.perez@example.com",
        "mensaje": "Contraseña actualizada exitosamente"
    },
    "message": "Contraseña actualizada correctamente"
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

### **Cerrar Sesión**
**Endpoint:** `POST /api/usuario/cerrar-sesion`  
**Descripción:** Cierra la session del usuario.

**Query Parameters (Obligatorio):**
- 'usuario_id': ID del usuario que se desea cerrar la sesión.

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
- 'nombre_proveedor': Nombre proveedor
- 'nrc' NRC del proveedor.
- 'telefono' Teléfono del proveedor.
- 'email' Email del solicitante.

**Response (success):**
```json
{
    "code": 0,
    "data": {
        "current_page": 1,
        "per_page": 10,
        "solicitudes": [
            {
                "email": "test@test.com",
                "estado": "PENDIENTE",
                "factura": {
                    "fecha_emision": "2024-11-01T10:00:00",
                    "fecha_otorga": "2024-11-01T11:00:00",
                    "fecha_vence": "2025-01-18T10:00:00",
                    "id": 1,
                    "monto": 1500.0,
                    "no_factura": "FAC001",
                    "proveedor": {
                        "correo_electronico": "contacto@technova.com",
                        "id": 1,
                        "max_factoring": "5000.00",
                        "min_factoring": "1000.00",
                        "nit": "NIT456789123",
                        "nombre_contacto": "Juan Pérez",
                        "nrc": "NRC12345",
                        "razon_social": "TechNova Solutions S.A.",
                        "telefono": "555-12345"
                    }
                },
                "id": 4,
                "id_estado": 1,
                "iva": 4.58,
                "nombre_cliente": "Eliazar Pasasin",
                "subtotal": 39.83,
                "total": 1460.17
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

**Query Parameters (Obligatorio):**
- 'id': Numero de la solicitud que se desea obtener los detalles.

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
        "solicitud": {
            "email": "test@test.com",
            "estado": "PENDIENTE",
            "factura": {
                "fecha_otorga": "01/11/2024",
                "fecha_vence": "18/01/2025",
                "id": 1,
                "monto": 1500.0,
                "no_factura": "FAC001",
                "pronto_pago": 35.25,
                "proveedor": {
                    "correo_electronico": "contacto@technova.com",
                    "id": 1,
                    "razon_social": "TechNova Solutions S.A.",
                    "telefono": "555-12345"
                }
            },
            "id": 4,
            "id_estado": 1,
            "iva": 4.58,
            "nombre_cliente": "Eliazar Pasasin",
            "subtotal": 39.83,
            "total": 1460.17
        }
    },
    "message": "Consulta exitosa"
}
```

### **Aprobar una solicitud**
**Endpoint:** `PUT /api/solicitud/aprobar`
**Descripción:** Cambia el estado de la solicitud a Aprobada y puede registrar información adicional sobre quién aprobó la solicitud.

**Query Parameters (Obligatorio):**
- 'id': Numero de la solicitud que se desea aprobar.

**Headers:**
```json
{
    "Authorization": "Bearer <access_token>"
}
```

**Body (JSON):**
```json
{
  "id_aprobador": 5, 
  "comentario": "Documentacion satisfactoria"
}
```

**Response:**
```json
{
    "code": 0,
    "data": {
        "solicitud": {
            "contacto": "555-12345",
            "email": "eliazar.rebollo23@gmail.com",
            "factura": {
                "id": 1,
                "monto": 1500.0,
                "no_factura": "FAC001",
                "proveedor": {
                    "id": 1,
                    "razon_social": "TechNova Solutions S.A."
                }
            },
            "fecha_aprobacion": "2024-12-04T16:12:34",
            "id": 6,
            "id_aprobador": 1,
            "id_estado": 2,
            "nombre_cliente": "Eliazar Antonio Rebollo Pasasin",
            "total": 1460.17
        }
    },
    "message": "Solicitud aprobada exitosamente. Correo de notificación enviado."
}
```

### **Denegar una solicitud**
**Endpoint:** `PUT /api/solicitud/denegar`
**Descripción:** Cambia el estado de la solicitud a Denegada y permite registrar una razón para la denegación.

**Query Parameters (Obligatorio):**
- 'id': Numero de la solicitud que se desea denegar.

**Headers:**
```json
{
    "Authorization": "Bearer <access_token>"
}
```

**Body (JSON):**
```json
{
  "comentario": "Documentación incompleta."  // (opcional) 
}

```

**Response:**
```json
{
    "code": 0,
    "data": {
        "solicitud": {
            "contacto": "555-12345",
            "email": "eliazar.rebollo23@gmail.com",
            "factura": {
                "id": 1,
                "monto": 1500.0,
                "no_factura": "FAC001",
                "proveedor": {
                    "id": 1,
                    "razon_social": "TechNova Solutions S.A."
                }
            },
            "id": 5,
            "id_estado": 3,
            "nombre_cliente": "Eliazar Antonio Rebollo Pasasin",
            "total": 1460.17
        }
    },
    "message": "Solicitud denegada exitosamente. Correo de notificación enviado."
}
```

### **Obtener métricas de solicitudes**
**Endpoint:** `GET /api/solicitud/panel-solicitudes`
**Descripción:** Devuelve las métricas de solicitudes, incluyendo el número de solicitudes aprobadas y pendientes.

**Query Parameters (opcional):**
- 'fecha_inicio', `fecha_fin`: Rango de fechas.

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
        "filtros_aplicados": {
            "fecha_fin": "2024-12-05",
            "fecha_inicio": "2024-12-01"
        },
        "solicitudes_aprobadas": 1,
        "solicitudes_sin_aprobar": 1,
        "total_solicitudes": 2
    },
    "message": "Métricas de solicitudes obtenidas con éxito"
}
```
