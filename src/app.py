import uvicorn as uvicorn
from fastapi import FastAPI

from .middlewares import request_handler
from .settings import api_settings as settings

app = FastAPI(title=settings.title, version="0.0.1")
app.middleware("http")(request_handler)


def run():
    uvicorn.run(
        app,
        host=settings.host,
        port=settings.port,
        log_level=settings.log_level.lower()
    )