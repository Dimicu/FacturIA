import logging
from datetime import datetime
from backend.all_supabase_db_connections import SupabaseDB_connection


db = SupabaseDB_connection()


def errores_backend(endpoint: str, error_message: str):
    error_data = {
        "timestamp": datetime.utcnow().isoformat(),
        "error_message": error_message,
        "endpoint": endpoint,
    }
    db.insert_monitoring("errores_logs", error_data)
    print("guardamos errores db")
