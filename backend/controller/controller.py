from fastapi import APIRouter
from backend.model.modelos import Usuario
from backend.services.services_usuario import services_user
from backend.services.services_facturas import services_factura

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
    services_factura.procesar_factura()


@router.post("/consulta-parseada")
def instrucciones():
    services_factura.consulta_parseada()
