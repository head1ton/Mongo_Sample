from src.database import collection
from src.exceptions import PersonNotFoundException
from src.models.person_create import PersonCreate
from src.models.person_read import PersonRead, PeopleRead
from src.models.person_update import PersonUpdate

from src.utils import get_time, get_uuid


__all__ = ("PeopleRepository", )


class PeopleRepository:
    @staticmethod
    def get(person_id: str) -> PersonRead:
        document = collection.find_one({"_id": person_id})
        if not document:
            raise PersonNotFoundException(person_id)
        return PersonRead(**document)

    @staticmethod
    def create(create: PersonCreate) -> PersonRead:
        document = create.dict()
        document["created"] = document["updated"] = get_time()
        document["_id"] = get_uuid()

        result = collection.insert_one(document)
        assert result.acknowledged

        return PeopleRepository.get(result.inserted_id)

    @staticmethod
    def list() -> PeopleRead:
        cursor = collection.find()
        return [PersonRead(**document) for document in cursor]

    @staticmethod
    def update(person_id: str, update: PersonUpdate):
        document = update.dict()
        document["updated"] = get_time()

        result = collection.update_one({"_id": person_id}, {"$set": document})
        if not result.modified_count:
            raise PersonNotFoundException(identifier=person_id)

    @staticmethod
    def delete(person_id: str):
        result = collection.delete_one({"_id": person_id})
        if not result.deleted_count:
            raise PersonNotFoundException(identifier=person_id)
