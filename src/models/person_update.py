from contextlib import suppress
from datetime import date
from typing import Optional

from pydantic import BaseModel

from src.models.address_read import AddressRead
from src.models.person import Person

__all__ = ("PersonUpdate", )


class PersonUpdate(BaseModel):
    name: Optional[str] = Person.name
    address: Optional[AddressRead] = Person.address_update
    birth: Optional[date] = Person.birth

    def dict(self, **kwargs):
        d = super().dict(**kwargs)
        with suppress(KeyError):
            d["birth"] = d.pop("birth").isoformat()
        return d

