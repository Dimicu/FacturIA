from fastapi import APIRouter
from backend.model.modelos import Usuario
from backend.services.services_usuario import services_user
from backend.services.services_facturas import services_factura
from fastapi import APIRouter, UploadFile, File

from backend.model.modelos import Usuario
from backend.services.services_usuario import services_user
import backend.services.services_facturas.services_factura

router = APIRouter()


@router.post("/login")
def login(usuario: Usuario):
    response_login = services_user.login(usuario)
    return response_login


@router.post("/registro")
def registro(usuario: Usuario):
    response_registro = services_user.registro(usuario)
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


@router.post("/procesar-factura")
async def procesar_factura():
    backend.services.services_facturas.services_factura.procesar_factura()


@router.post("/consulta-parseada")
def instrucciones():
    backend.services.services_facturas.services_factura.consulta_parseada()


@router.post("/upload_factura")
async def upload_factura(file: UploadFile = File(...)):

    content = await file.read()  # Leer el contenido del archivo
    file_size = len(content)  # Obtener el tamaño del archivo correctamente

    response = (
        await backend.services.services_facturas.services_factura.serv_subir_factura(
            content, file.filename, file.content_type
        )
    )  # Lee el archivo y pasa el nombre
    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "size": file_size,
    }
