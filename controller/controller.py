from fastapi import APIRouter
from model.modelos import Usuario
from services.services_usuario import services_user
import services.services_facturas.services_factura

router = APIRouter()


@router.post("/login")
def login(usuario: Usuario):
    response_login = services_user.login_o_registro(usuario)
    return response_login


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
    services.services_facturas.services_factura.procesar_factura()


@router.post("/consulta-parseada")
def instrucciones():
    services.services_facturas.services_factura.consulta_parseada()
