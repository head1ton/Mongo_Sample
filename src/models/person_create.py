from src.models.address import Address
from src.models.person import Person
from src.models.person_update import PersonUpdate

__all__ = ("PersonCreate", )


class PersonCreate(PersonUpdate):
    name: str = Person.name
    address: Address = Person.address