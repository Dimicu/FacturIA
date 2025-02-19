from fastapi import APIRouter
from model.modelos import Usuario
from services.services_usuario import services_user


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
