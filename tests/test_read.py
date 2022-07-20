from fastapi import status

from src.utils import get_uuid
from tests.base import BaseTest
from tests.utils import get_existing_person


class TestGet(BaseTest):
    def test_get_existing_person(self):
        """
        존재한다면 반환
        """
        person = get_existing_person()

        response = self.get_person(person.person_id)
        assert response.json() == person.dict()

    def test_get_nonexisting_person(self):
        """
        존재하지 않는 person 반환. 404 오류 및 식별자 반환
        """
        person_id = get_uuid()

        response = self.get_person(person_id, statuscode=status.HTTP_404_NOT_FOUND)
        assert response.json()["identifier"] == person_id


class TestList(BaseTest):
    def test_list_people(self):
        """
        모든 person 반환
        """
        people = [get_existing_person() for _ in range(4)]

        response = self.list_people()
        assert response.json() == [p.dict() for p in people]