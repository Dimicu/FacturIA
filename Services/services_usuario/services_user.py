from supabase_db import SupabaseDB
from fastapi import FastAPI
from model.modelos import Usuario


db = SupabaseDB()
app = FastAPI()


def login_o_registro(usuario: Usuario):

    if db.login_usuario(usuario.email, usuario.password):
        return {"mensaje": f"Bienvenido {usuario.email} a FacturAi."}
    else:
        respuesta = input(
            "Usuario no encontrado o datos incorrectos. ¿Quieres registrarte? (s/n): "
        ).lower()
        if respuesta == "s":
            db.registrar_usuario(usuario.email, usuario.password)
            return {"mensaje": "Usuario registrado correctamente"}
        else:
            return {"mensaje": "No se ha registrado al usuario. Intenta de nuevo."}


def actualizar_password(usuario: Usuario):

    response_actualizar_datos = db.actualizar_Users(
        usuario.email, usuario.password, usuario.role
    )

    if "error" in response_actualizar_datos:
        return "No se ha podido actualizar los datos "


def borrar_usuarios(id: int):
    response_delete = db.supabase.table("users").delete().eq("id", id).execute()

    return response_delete.data[0]