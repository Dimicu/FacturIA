from fastapi import APIRouter
from backend.model.modelos import Usuario
from backend.services.services_usuario import services_user
from backend.services.services_facturas import services_factura
from fastapi import APIRouter, UploadFile, File

from model.modelos import Usuario
from services.services_usuario import services_user
import services.services_facturas.services_factura

router = APIRouter()


@router.post("/login")
async def login(usuario: Usuario):
    services_user.login_o_registro(usuario)


@router.put("/usuarios")
async def actualizar_datos_usuario(usuario: Usuario):
    services_user.actualizar_password(usuario)


@router.delete("/usuarios/{id}")
async def eliminar_usuario_id(id):
    services_user.borrar_usuarios(id)

@router.post("/procesar-factura")
async def procesar_factura():
    services.services_facturas.services_factura.procesar_factura()

@router.post("/consulta-parseada")
def instrucciones():
    services.services_facturas.services_factura.consulta_parseada()

@router.post("/upload_factura")
async def upload_factura(file:UploadFile = File(...)):

    content = await file.read()  # Leer el contenido del archivo
    file_size = len(content)  # Obtener el tamaño del archivo correctamente

    response = await services.services_facturas.services_factura.serv_subir_factura(content, file.filename, file.content_type) # Lee el archivo y pasa el nombre
    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "size": file_size
    }