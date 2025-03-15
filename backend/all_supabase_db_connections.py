import os
import logging
import bcrypt
from dotenv import load_dotenv


# from multipart import file_path
from supabase import create_client, Client


from backend.utils.throw_json_error import throw_json_error


class SupabaseDB_connection:
    def __init__(self):
        """Initialize the Supabase client with credentials from environment variables."""

        load_dotenv()
        SUPABASE_URL = os.getenv("SUPABASE_URL")
        SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
        SUPABASE_BUCKET_NAME = os.getenv("SUPABASE_BUCKET_NAME")
        SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")
        SUPABASE_PROJECT_ID = os.getenv("SUPABASE_PROJECT_ID")

        if not SUPABASE_URL or not SERVICE_ROLE_KEY:
            raise ValueError(
                "Missing Supabase URL or Service Role Key in environment variables."
            )

        # Initialize Supabase client
        self.supabase: Client = create_client(SUPABASE_URL, SERVICE_ROLE_KEY)

    # Metodos CRUD tabla facturas
    async def insertar_factura_db(self, data: dict, id, nombre_imagen, tipo_factura):

        response = (
            self.supabase.table("facturas")
            .insert(
                {
                    "datos_factura": data,
                    "users_id": id,
                    "nombre_imagen": nombre_imagen,
                    "tipo_de_factura": tipo_factura,
                }
            )
            .execute()
        )

        if response.data == 201:
            return "Factura guardada con éxito"
        elif response.data == 400:
            return throw_json_error("Error en los datos proporcionado", 400)

    def actualizar_factura(self, email: str, updates: dict):

        response = (
            self.supabase.table("facturas").update(updates).eq("email", email).execute()
        )
        return response

    def factura_db_supabase(self, email: str):

        user_response = (
            self.supabase.table("users").select("id").eq("email", email).execute()
        )

        if not user_response.data:
            return {"error": "User not found"}

        user_id = user_response.data[0]["id"]

        response = (
            self.supabase.table("facturas")
            .select("id_factura, datos_factura, nombre_imagen")
            .filter("users_id", "eq", user_id)
            .execute()
        )

        return response

    # Metodos tabla de costes
    def coste_guardar_fact_tabla(self, modelo, total_tokens, cost):
        data = {
            "model": modelo,
            "total_tokens": total_tokens,
            "cost": cost,
        }
        self.supabase.table("openai_requests").insert(data).execute()

    # Metodos de imagenes
    async def sp_subir_imagen_factura(self, file_data, filename, content_type):
        """Sube una factura a Supabase Storage."""
        # Subir archivo a Supabase Storage
        response = self.supabase.storage.from_("imagenes_facturas").upload(
            path=filename,  # Se guarda con el mismo nombre del archivo
            file=file_data,
            file_options={"content-type": content_type},  # Mantener el tipo de archivo
        )

    def sp_tomar_imagen_storage(self, nombre_imagen):
        try:
            signed_url_data = self.supabase.storage.from_(
                "imagenes_facturas"
            ).create_signed_url(nombre_imagen, expires_in=3600 * 8)

            if not signed_url_data or "signedURL" not in signed_url_data:
                print(f"Imagen '{nombre_imagen}' no encontrada en Supabase.")
                return None  # Se manejará en el servicio y el controller

            signed_url = signed_url_data["signedURL"]
            return signed_url

        except Exception as e:
            print(f"Error en Supabase: {str(e)}")
            return None

    # Metodos CRUD usuarios
    def registrar_usuario(self, email: str, password: str):
        try:

            respuesta_si_existe = (
                self.supabase.table("users")
                .select("email")
                .eq("email", email)
                .execute()
            )

            if respuesta_si_existe.data and len(respuesta_si_existe.data) > 0:
                emailCheckeado = respuesta_si_existe.data[0]

                if emailCheckeado["email"] == email:
                    return throw_json_error(
                        f"El correo electrónico {email} ya está registrado.", 400
                    ).to_json()

            else:
                password_hash = bcrypt.hashpw(
                    password.encode("utf-8"), bcrypt.gensalt()
                )

                respuesta_insertar = (
                    self.supabase.table("users")
                    .insert(
                        {
                            "email": email,
                            "password": password_hash.decode("utf-8"),
                            "role": "reader",
                        }
                    )
                    .execute()
                )
                if respuesta_insertar.data:

                    return throw_json_error(
                        f"Usuario registrado correctamente con el correo {email}", 201
                    ).to_json()

                else:
                    return throw_json_error(
                        "No se pudo registrar el usuario debido a un error en la base de datos",
                        500,
                    ).to_json()

        except Exception as e:
            return throw_json_error(
                f"Hubo un problema al registrar el usuario(backend) {str(e)}", 500
            ).to_json()

    def login_usuario(self, email: str, password: str):

        response = self.supabase.table("users").select("*").eq("email", email).execute()

        if response.data:
            user = response.data[0]

            if bcrypt.checkpw(
                password.encode("utf-8"), user["password"].encode("utf-8")
            ):

                return throw_json_error("Login exitoso", 200).to_json()
            else:
                return throw_json_error(
                    "Contraseña incorrecta o Usuario", 400
                ).to_json()

        else:
            return throw_json_error("Usuario no registrado", 404).to_json()

    def actualizar_Users(self, email, password, role):

        response_check_email = (
            self.supabase.table("users").select("email").eq("email", email).execute()
        )

        if not response_check_email.data:
            return {"error": "Usuario no encontrado"}

        nueva_contraseña = bcrypt.hashpw(
            password.encode("utf-8"), bcrypt.gensalt()
        ).decode("utf-8")

        response_update = (
            self.supabase.table("users")
            .update({"password": nueva_contraseña, "role": role})
            .eq("email", email)
            .execute()
        )

        return response_update.data[0]

    def eliminar_users(self, id):

        response_check_id = (
            self.supabase.table("users").select("id").eq("id", id).execute()
        )

        if not response_check_id.data:

            return {"error": f"Usuario con ID {id} no encontrado"}

        response_delete = self.supabase.table("users").delete().eq("id", id).execute()

        if response_delete.data:

            deleted_user = response_delete.data[0]
            return {
                "message": f"Usuario con ID {deleted_user['id']} eliminado correctamente"
            }
        else:
            return {"error": "No se pudo eliminar el usuario"}

    def obtener_users_id_por_email(self, email):
        response = (
            self.supabase.table("users").select("id").eq("email", email).execute()
        )
        if not response.data:
            return {"message": f"El {email} no existe, debes registarte"}

        return response.data[0]["id"]

    # metodos monitoreo
    def insert_monitoring(self, table: str, data: dict):

        response = self.supabase.table(table).insert(data).execute()
        return response
