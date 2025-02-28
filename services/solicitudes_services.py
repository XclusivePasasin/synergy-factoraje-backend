from io import BytesIO
import pandas as pd
from utils.db import db
from models.solicitudes import Solicitud
from models.facturas import Factura
from models.proveedores_calificados import ProveedorCalificado
from flask import send_file

def actualizar_solicitudes(lista_ids):
    """
    Actualiza el estado de solicitudes a 'Procesada' (id_estado = 4) solo si están en la lista de valores unicos recibida.
    """
    if not lista_ids or not isinstance(lista_ids, list):
        return None, "Debe proporcionar una lista de valores unicos válida"

    solicitudes_a_procesar = Solicitud.query.filter(Solicitud.id.in_(lista_ids), Solicitud.id_estado != 4).all()
    
    if not solicitudes_a_procesar:
        return None, "No se encontraron solicitudes para actualizar"

    for solicitud in solicitudes_a_procesar:
        solicitud.id_estado = 4
    
    db.session.commit()
    return print(f'Se procesaron:{len(solicitudes_a_procesar)} solicitudes.'), None  


def exportar_solicitudes(lista_ids, formato="excel"):
    """
    Extrae la informacion de las solicitudes de acuerdo a la lista de valores unicos que se recibe y 
    devuelve un archivo de Excel o CSV con la informacion de las solicitudes para su procesamiento y desembolso.
    """
    query = db.session.query(
        Solicitud.id, Solicitud.nombre_cliente, Solicitud.contacto, Solicitud.email,
        Solicitud.total, Solicitud.fecha_solicitud, Solicitud.fecha_aprobacion,
        Factura.no_factura.label("numero_factura"), Factura.monto.label("monto_factura"),
        Factura.fecha_emision.label("fecha_factura"),
        ProveedorCalificado.razon_social.label("nombre_proveedor"), 
        ProveedorCalificado.nombre_contacto.label("contacto_proveedor"),
        ProveedorCalificado.correo_electronico.label("email_proveedor")
    ).join(Factura, Solicitud.id_factura == Factura.id)\
     .join(ProveedorCalificado, Factura.id_proveedor == ProveedorCalificado.id)\
     .filter(Solicitud.id.in_(lista_ids))

    resultados = query.all()

    data = [{
        "ID Solicitud": r.id,
        "Cliente": r.nombre_cliente,
        "Contacto Cliente": r.contacto,
        "Email Cliente": r.email,
        "Total": r.total,
        "Fecha Solicitud": r.fecha_solicitud.strftime("%Y-%m-%d %H:%M:%S") if r.fecha_solicitud else None,
        "Fecha Aprobación": r.fecha_aprobacion.strftime("%Y-%m-%d %H:%M:%S") if r.fecha_aprobacion else None,
        "N° Factura": r.numero_factura,
        "Monto Factura": r.monto_factura,
        "Fecha Factura": r.fecha_factura.strftime("%Y-%m-%d") if r.fecha_factura else None,
        "Proveedor": r.nombre_proveedor,
        "Contacto Proveedor": r.contacto_proveedor,
        "Email Proveedor": r.email_proveedor
    } for r in resultados]

    df = pd.DataFrame(data)

    output = BytesIO()
    if formato == "csv":
        df.to_csv(output, index=False, encoding="utf-8-sig")
        output.seek(0)
        mimetype = "text/csv"
        filename = "solicitudes_procesadas.csv"
    else:
        with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
            df.to_excel(writer, index=False, sheet_name="Solicitudes")
        output.seek(0)
        mimetype = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        filename = "solicitudes_procesadas.xlsx"

    return send_file(output, download_name=filename, as_attachment=True, mimetype=mimetype)
