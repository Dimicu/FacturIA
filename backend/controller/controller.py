import io
import uuid
from http.client import HTTPResponse, HTTPConnection, HTTPException

from PIL.Image import Image
from fastapi import APIRouter, HTTPException
from starlette.responses import JSONResponse

from backend.supabase_db import SupabaseDB
from backend.model.modelos import Usuario
from backend.services.services_facturas import services_factura
from backend.services.services_usuario import services_user
from backend.services.services_facturas import services_factura
from fastapi import APIRouter, UploadFile, File
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


@router.post("/facturas/completo")
async def guardar_fact_completa(file: UploadFile = File(...), email=str):

    users_id = db.obtener_users_id_por_email(email)

    # Se crea nombre de archivo unico
    nombre_imagen = f"{uuid.uuid4()}_{file.filename}"
    # Leer el contenido de bytes de la imagen
    content = await file.read()
    # Extrae texto de la imagen
    texto_extraido = await services_factura.extraer_texto_imagen_subida(
        content
    )
    # Envia ese texto junto con un contexto e instrucciones a la API
    respuesta_api = (
       services_factura.srv_interpretar_factura(
            texto_extraido
        )
    )
    # Enviar la respuesta de la API a la base de datos añadiendo un campo de nombre para la imagen
    #respuesta_api["nombre_imagen"] = nombre_imagen
    await services_factura.serv_guardar_datos_factura_json(respuesta_api, users_id, nombre_imagen)
    await backend.services.services_facturas.services_factura.serv_subir_imagen_factura(
        content, nombre_imagen, file.content_type
    )
    return {"message": "Factura guardada correctamente"}


@router.get("/facturas/{email}")
def factura_db_controller(email):
    response = services_factura.factura_db_services(email)

    return response
