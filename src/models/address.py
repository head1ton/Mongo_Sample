from time import time
from uuid import uuid4

from pydantic import Field


__all__ = ("Address", )

_string = dict(min_length=1)


class Address:
    street = Field(
        description="Main address line",
        example="22nd Bunker Hill Avenue",
        **_string
    )
    city = Field(
        description="City",
        example="Hamburg",
        **_string
    )
    state = Field(
        description="State, province and/or region",
        example="Mordor",
        **_string
    )
    zip_code = Field(
        description="Postal/ZIP code",
        example="19823",
        **_string
    )
