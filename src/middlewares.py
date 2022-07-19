

__all__ = ("request_handler",)

from fastapi import Request

from src.exceptions import BaseAPIException


async def request_handler(request: Request, call_next):
    """
    예외적인 오류 처리를 위한 미들웨어
    """
    try:
        return await call_next(request)

    except Exception as ex:
        if isinstance(ex, BaseAPIException):
            return ex.response()

        raise ex