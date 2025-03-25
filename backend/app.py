import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import uvicorn
from fastapi import FastAPI
from backend.controller.controller import router
from monitoring.rendimiento import measure_request_time
import logging


app = FastAPI()
app.include_router(router)
logging.basicConfig(level=logging.ERROR)
app.middleware("http")(measure_request_time)

if __name__ == "__main__":
    # Obtener el puerto de la variable de entorno PORT, si no está configurada, usar 8000 como valor predeterminado
    port = int(os.environ.get("PORT", 8000))

    # Ejecutar Uvicorn con el host 0.0.0.0 y el puerto configurado
    uvicorn.run(app, host="0.0.0.0", port=port)
