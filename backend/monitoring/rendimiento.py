import time
from fastapi import Request
from backend.all_supabase_db_connections import SupabaseDB_connection
from datetime import datetime


db = SupabaseDB_connection()


async def measure_request_time(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time

    log_data = {
        "timestamp": datetime.utcnow().isoformat(),
        "endpoint": request.url.path,
        "method": request.method,
        "response_time": duration,
    }
    db.insert_monitoring("rendimiento_logs", log_data)

    return response
