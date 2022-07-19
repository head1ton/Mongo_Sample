from datetime import datetime
from typing import Optional, List

import pydantic
from dateutil.relativedelta import relativedelta

from src.models.person import Person
from src.models.person_create import PersonCreate

__all__ = ("PersonRead", "PeopleRead")


class PersonRead(PersonCreate):
    person_id: str = Person.person_id
    age: Optional[int] = Person.age
    created: int = Person.created
    updated: int = Person.updated

    @pydantic.root_validator(pre=True)
    def _set_person_id(cls, data):
        document_id = data.get("_id")
        if document_id:
            data["person_id"] = document_id
        return data

    @pydantic.root_validator()
    def _set_age(cls, data):
        birth = data.get("birth")
        if birth:
            today = datetime.now().date()
            data["age"] = relativedelta(today, birth).years
        return data

    class Config(PersonCreate.Config):
        extra = pydantic.Extra.ignore


PeopleRead = List[PersonRead]

