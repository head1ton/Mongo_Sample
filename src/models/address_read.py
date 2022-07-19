from src.models.common import BaseModel
from src.models.address import Address


__all__ = ("AddressRead", )


class AddressRead(BaseModel):
    street: str = Address.street
    city: str = Address.city
    state: str = Address.state
    zip_code: str = Address.zip_code