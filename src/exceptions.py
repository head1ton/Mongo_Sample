from fastapi import status
from fastapi.responses import JSONResponse
from loguru import logger

from src.models.errors import BaseError


class BaseAPIException(Exception):
    message = "Generic error"
    code = status.HTTP_500_INTERNAL_SERVER_ERROR
    model = BaseError

    def __init__(self, **kwargs):
        kwargs.setdefault("message", self.message)
        self.message = kwargs["message"]
        self.data = self.model(**kwargs)
        logger.debug(f"message ====> {self.message}, data ====> {self.data}")

    def __str__(self):
        return self.message

    def response(self):
        return JSONResponse(
            content=self.data.dict(),
            status_code=self.code
        )

    @classmethod
    def response_model(cls):
        return {cls.code: {"model": cls.model}}
