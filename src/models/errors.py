from pydantic import BaseModel, Field

__all__ = ("BaseError")


class BaseError(BaseModel):
    message: str = Field(..., description="Error message or description")\
