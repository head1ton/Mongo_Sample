from fastapi import FastAPI

from .middlewares import request_handler
from .settings import api_settings as settings

app = FastAPI(title=settings.title, version="0.0.1")
app.middleware("http")(request_handler)


