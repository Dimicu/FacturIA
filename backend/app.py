import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import uvicorn
from fastapi import FastAPI
from backend.controller.controller import router


app = FastAPI()
app.include_router(router)


if __name__ == "__main__":

    uvicorn.run(app, host="127.0.0.1", port=8000)
