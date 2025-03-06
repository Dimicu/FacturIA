import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import uvicorn
from fastapi import FastAPI
from backend.controller.controller import router


app = FastAPI()
app.include_router(router)


if __name__ == "__main__":
    # Obtener el puerto de la variable de entorno PORT, si no está configurada, usar 8000 como valor predeterminado
    port = int(os.environ.get("PORT", 8000))

    # Ejecutar Uvicorn con el host 0.0.0.0 y el puerto configurado
    uvicorn.run(app, host="0.0.0.0", port=port)
