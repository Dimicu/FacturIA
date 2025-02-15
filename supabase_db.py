import os
from dotenv import load_dotenv
from supabase import create_client, Client


class SupabaseDB:
    def __init__(self):
        """Initialize the Supabase client with credentials from environment variables."""

        load_dotenv()
        SUPABASE_URL = os.getenv("SUPABASE_URL")
        SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
        print(SUPABASE_URL)

        if not SUPABASE_URL or not SERVICE_ROLE_KEY:
            raise ValueError("Missing Supabase URL or Service Role Key in environment variables.")

        # Initialize Supabase client
        self.supabase: Client = create_client(SUPABASE_URL, SERVICE_ROLE_KEY)

    def insertar_factura(self, data: dict):
        """Insert a new invoice record into the 'facturas' table."""
        response = self.supabase.table("facturas").insert(data).execute()
        return response

    def actualizar_factura(self, email: str, updates: dict):
        """Update an invoice record in the 'facturas' table based on the user's email."""
        response = (
            self.supabase.table("facturas")
            .update(updates)
            .eq("email", email)
            .execute()
        )
        return response

    def obtener_factura(self, email: str):
        """Get invoice data from the 'facturas' table based on the user's email."""
        response = (
            self.supabase.table("facturas")
            .select("*")
            .eq("email", email)
            .execute()
        )
        return response

    def insertar_datos_coste(self, modelo,input_tokens,output_tokens, total_tokens, cost):
        data = {
            "model": modelo,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "total_tokens": total_tokens,
            "cost": cost
        }
        self.supabase.table("openai_requests").insert(data).execute()
