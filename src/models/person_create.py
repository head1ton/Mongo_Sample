from src.models.person_update import PersonUpdate
from src.models.address_read import AddressRead
from src.models.person import Person


__all__ = ("PersonCreate", )


class PersonCreate(PersonUpdate):
    name: str = Person.name
    address: AddressRead = Person.address
