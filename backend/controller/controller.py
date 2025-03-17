import io
import uuid
import json
from http.client import HTTPResponse, HTTPConnection, HTTPException

from PIL.Image import Image
from fastapi import APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse

from backend.supabase_db import SupabaseDB
from backend.model.modelos import Usuario
from backend.services.services_facturas import services_factura
from backend.services.services_usuario import services_user
from backend.services.services_facturas import services_factura
from fastapi import APIRouter, UploadFile, File, Form, Body

import streamlit as st


import backend.services.services_facturas.services_factura


db = SupabaseDB()
router = APIRouter()


@router.post("/login")
def login(usuario: Usuario):
    response_login = services_user.login(dict(usuario))
    return response_login


@router.post("/registro")
def registro(usuario: Usuario):
    response_registro = services_user.registro(dict(usuario))
    print("desde controller", response_registro)
    return response_registro


@router.put("/usuarios")
async def actualizar_datos_usuario(usuario: Usuario):
    services_user.actualizar_password(usuario)
    return "usuario actualizado"


@router.delete("/usuarios/{id}")
async def eliminar_usuario_id(id: int):
    services_user.borrar_usuarios(id)
    return "usuario eliminado"


@router.post("/facturas/api/json")
def extraer_json_formateado(texto):
    services_factura.srv_interpretar_factura(texto)


@router.post("/imagenes/storage")
async def guardar_fact_storage(file: UploadFile = File(...)):

    content = await file.read()  # Leer el contenido del archivo
    nombre_imagen = f"{uuid.uuid4()}_{file.filename}"

    await services_factura.serv_subir_imagen_factura(
        content, nombre_imagen, file.content_type
    )


@router.post("/imagenes/{nombre_imagen}")
def obtener_imagen_storage(nombre_imagen):
    url_imagen = services_factura.serv_tomar_imagen_storage(nombre_imagen)

    if not url_imagen:
        raise HTTPException(status_code=404, detail="Imagen no encontrada en Supabase")
    return {"url": url_imagen}


@router.post("/facturas/file")
async def guardar_fact_completa(
    file: UploadFile = File(...),
    email: str = Form(...),
):
    db.obtener_users_id_por_email(email)
    content = await file.read()
    texto_extraido = await services_factura.extraer_texto_imagen_subida(content)
    respuesta_api = services_factura.srv_interpretar_factura(texto_extraido)

    print("api", type(respuesta_api))

    return respuesta_api


@router.post("/facturas/completa")
async def guardar_bd_factura(
    email: str = Form(...),
    file: UploadFile = File(...),
    tipo_factura: str = Form(...),
    json_front_modified: str = Form(...),
):

    json_formateado = json.loads(json_front_modified)
    user_id = db.obtener_users_id_por_email(email)
    content_changed = await file.read()
    nombre_imagen = f"{uuid.uuid4()}_{file.filename}"

    await services_factura.serv_guardar_datos_factura_json(
        json_formateado, user_id, nombre_imagen, tipo_factura
    )

    await backend.services.services_facturas.services_factura.serv_subir_imagen_factura(
        content_changed, nombre_imagen, file.content_type
    )


    return JSONResponse(
        status_code=200,
        content={
            "message": "Factura guardada correctamente",
            "Factura": {"Usuario": email, "Tipo de factura": tipo_factura},
            "Balance" : "Su balance ha sido actualizado con exito"
        },
    )


@router.get("/facturas/{email}")
def factura_db_controller(email):
    response = services_factura.factura_db_services(email)
    return response

@router.get("/facturas/balance/{email}")
def obtener_factura_balance(email):
    try:
        response = services_factura.serv_obtener_balance(email)
        return jsonable_encoder(response.data)
    except HTTPException as http_exc:
        # Si ya es una HTTPException, la relanzamos sin modificarla
        raise http_exc
    except Exception as e:
        # Lanzar un error 500 sin exponer detalles internos
        raise HTTPException(status_code=500, detail="Ocurrió un error inesperado. Inténtalo más tarde.")

"""
@router.put("/facturas/actualizacion/{id}")
def actualizar_balance(id,tipo_factura, total):
    try:
        response = services_factura.serv_actualizar_balance(id, tipo_factura, total)
    except Exception as e:
        print(f"error: {e}")
    return jsonable_encoder(response)"""