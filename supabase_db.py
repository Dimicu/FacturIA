import json
import os
import bcrypt
from dotenv import load_dotenv
from supabase import create_client, Client


class SupabaseDB:
    def __init__(self):
        """Initialize the Supabase client with credentials from environment variables."""

        load_dotenv()
        SUPABASE_URL = os.getenv("SUPABASE_URL")
        SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

        if not SUPABASE_URL or not SERVICE_ROLE_KEY:
            raise ValueError(
                "Missing Supabase URL or Service Role Key in environment variables."
            )

        # Initialize Supabase client
        self.supabase: Client = create_client(SUPABASE_URL, SERVICE_ROLE_KEY)

    def insertar_factura(self, data: dict):

        response = self.supabase.table("facturas").insert(data).execute()
        return response

    def actualizar_factura(self, email: str, updates: dict):

        response = (
            self.supabase.table("facturas").update(updates).eq("email", email).execute()
        )
        return response

    def obtener_factura(self, email: str):

        response = (
            self.supabase.table("facturas").select("*").eq("email", email).execute()
        )
        return response

    def insertar_datos_coste(
        self, modelo, input_tokens, output_tokens, total_tokens, cost
    ):
        data = {
            "model": modelo,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "total_tokens": total_tokens,
            "cost": cost,
        }
        self.supabase.table("openai_requests").insert(data).execute()


    def registrar_usuario(self, email: str, password: str):

        respuesta_si_existe = (
            self.supabase.table("users").select("*").eq("email", email).execute()
        )

        if respuesta_si_existe.data:
            print(f"El correo electrónico {email} ya está registrado.")
        else:
            password_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

        self.supabase.table("users").insert(
            {
                "email": email,
                "password": password_hash.decode("utf-8"),
                "role": "reader",
            }
        ).execute()
        print(f"{email} te has registrado correctamente.")

    def login_usuario(self, email: str, password: str):
        response = self.supabase.table("users").select("*").eq("email", email).execute()

        if response.data:
            user = response.data[0]
            if bcrypt.checkpw(
                password.encode("utf-8"), user["password"].encode("utf-8")
            ):
                print(f"Bienvenido, {user['email']}")
                return True
            else:
                print("Datos incorrectos")
                return False
        else:
            print("Usuario no registrado, debe registrarse")
            return False
          
    def traer_datos(self):
        # Hacemos la consulta a la tabla 'facturas' para obtener el campo 'datos_factura'
        response = self.supabase.table("facturas").select("datos_factura->emisor->nombre").execute()
        response2 = self.supabase.table("facturas").select("datos_factura->datos_factura->emisor->nombre").execute()

        print(response)
        print(response2)

