from backend.supabase_db import SupabaseDB
from fastapi import FastAPI
from backend.model.modelos import Usuario


db = SupabaseDB()
app = FastAPI()


def login(usuario: dict):

    email = usuario.get("email", "").lower()
    password = usuario.get("password", "")

    response_login_o_registro = db.login_usuario(email, password)
    return response_login_o_registro


def registro(usuario: dict):

    email = usuario.get("email", "").lower()
    password = usuario.get("password", "")

    response_registro = db.registrar_usuario(email, password)
    print("desde services", response_registro)
    return response_registro


def actualizar_password(usuario: Usuario):

    response_actualizar_datos = db.actualizar_Users(
        usuario.email, usuario.password, usuario.role
    )

    if "error" in response_actualizar_datos:
        return "No se ha podido actualizar los datos "


def borrar_usuarios(id: int):
    response_delete = db.supabase.table("users").delete().eq("id", id).execute()

    return response_delete.data[0]
