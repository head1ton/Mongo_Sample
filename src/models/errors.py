from pydantic import BaseModel, Field

__all__ = ("BaseError", "BaseIdentifiedError", "NotFoundError", )


class BaseError(BaseModel):
    message: str = Field(..., description="Error message or description")


class BaseIdentifiedError(BaseError):
    pass


class NotFoundError(BaseIdentifiedError):
    pass

