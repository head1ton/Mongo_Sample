from fastapi import status
from fastapi.responses import JSONResponse
from loguru import logger

from src.models.errors import BaseError, NotFoundError, BaseIdentifiedError


__all__ = (
    "BaseAPIException", "BaseIdentifiedException",
    "NotFoundException", "PersonNotFoundException"
)


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


class BaseIdentifiedException(BaseAPIException):
    message = "Entity error"
    code = status.HTTP_500_INTERNAL_SERVER_ERROR
    model = BaseIdentifiedError

    def __init__(self, identifier, **kwargs):
        super().__init__(identifier=identifier, **kwargs)


class NotFoundException(BaseIdentifiedException):
    message = "The entity does not exist"
    code = status.HTTP_404_NOT_FOUND
    model = NotFoundError


class PersonNotFoundException(NotFoundException):
    message = "The person does not exist"

