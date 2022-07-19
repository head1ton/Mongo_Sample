from pydantic import Field

from src.utils import get_uuid, get_time

__all__ = ("Person", )

_string = dict(min_length=1)

_unix_ts = dict(example=get_time())


class Person:
    name = Field(
        description="Full name of this person",
        example="John Smith",
        **_string
    )
    address = Field(
        description="Address object where this person live"
    )
    address_update = Field(
        description=f"{address.description}. When updating, the whole Address object is required, as it gets replaced"
    )
    birth = Field(
        description="Date of birth, in format YYYY-MM-DD, or Unix timestamp",
        example="1999-12-31"
    )
    age = Field(
        description="Age of this person, if date of birth is specified",
        example=20
    )
    person_id = Field(
        description="Unique identifier of this person in the database",
        example=get_uuid(),
        min_length=36,
        max_length=36
    )
    created = Field(
        alias="created",
        description="When the person was registered (Unix timestamp)",
        **_unix_ts
    )
    updated = Field(
        alias="updated",
        description="When the person was updated for the last time (Unix timestamp)",
        **_unix_ts
    )
