from datetime import datetime
from random import randint

from src.models import PersonCreate, AddressRead
from src.repositories import PeopleRepository
from src.utils import get_uuid


def get_address(**kwargs):
    return AddressRead(**{
        "street": get_uuid(),
        "city": get_uuid(),
        "state": get_uuid(),
        "zip_code": randint(1000, 10000),
        **kwargs
    })


def get_person_create(**kwargs):
    return PersonCreate(**{
        "name": get_uuid(),
        "address": get_address(),
        "birth": datetime.now().date(),
        **kwargs
    })


def get_existing_person(**kwargs):
    return PeopleRepository.create(get_person_create(**kwargs))
