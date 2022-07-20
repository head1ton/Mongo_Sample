from datetime import datetime
from random import randint

import pydantic
from dateutil.relativedelta import relativedelta
from freezegun import freeze_time
from starlette import status

from src.models import PersonCreate, PersonRead, PersonUpdate
from src.repositories import PeopleRepository
from src.utils import get_uuid
from tests.base import BaseTest
from tests.utils import get_person_create, get_existing_person


class PersonAsCreate(PersonCreate):
    """
    PersonRead를 PersonCreate로 변환하는데 사용.
    API가 반환한 응답과 전송된 객체 생성을 비교
    """
    class Config(PersonCreate.Config):
        extra = pydantic.Extra.ignore


class TestCreate(BaseTest):
    def test_create_person(self):
        """
        person 생성
        """
        create = get_person_create().dict()

        response = self.create_person(create)
        response_as_create = PersonAsCreate(**response.json())
        assert response_as_create.dict() == create

    def test_create_person_assert_birth_age(self):
        """
        랜덤으로 생성된 숫자로 생년월일 만들어  person 생성
        """
        expected_age = randint(5, 25)
        today = datetime.now().date()
        birth = today - relativedelta(years=expected_age)
        create = get_person_create(birth=birth).dict()

        response = self.create_person(create)
        response_as_read = PersonRead(**response.json())

        assert response_as_read.birth == birth
        assert response_as_read.age == expected_age

    def test_create_person_without_birth(self):
        """
        생년월일이 없는 사람을 만듬
        """
        create = get_person_create(birth=None).dict()

        response = self.create_person(create)
        response_as_read = PersonRead(**response.json())

        assert response_as_read.birth is None
        assert response_as_read is None

    def test_timestamp_created_updated(self):
        iso_timestamp = "2020-01-01T00:00:00+00:00"
        expected_timestamp = int(datetime.fromisoformat(iso_timestamp).timestamp())

        with freeze_time(iso_timestamp):
            create = get_person_create()
            result = PeopleRepository.create(create)

        assert result.created == result.updated
        assert result.created == expected_timestamp


class TestDelete(BaseTest):
    def test_delete_person(self):
        """
        person 삭제
        """
        person = get_existing_person()

        self.delete_person(person.person_id)
        self.get_person(person.person_id, statuscode=status.HTTP_404_NOT_FOUND)

    def test_delete_nonexisting_person(self):
        """
        존재하지 않는 person 삭제. 404 오류 및 식별자 반환.
        """
        person_id = get_uuid()

        response = self.delete_person(person_id, statuscode=status.HTTP_404_NOT_FOUND)
        assert response.json()["identifier"] == person_id


class TestUpdate(BaseTest):
    def test_update_person_single_attribute(self):
        """
        이름을 업데이트하고 반환
        """
        person = get_existing_person()

        new_name = get_uuid()
        update = PersonUpdate(name=new_name)
        self.update_person(person.person_id, update.dict())

        read = PersonRead(**self.get_person(person.person_id).json())
        assert read.name == new_name
        assert read.dict() == {**person.dict(), "name": new_name, "updated": read.updated}

    def test_update_nonexisting_person(self):
        """
        존재하지 않는 person 이름 업데이트. 404 오류 및 식별자 반환
        """
        person_id = get_uuid()
        update = PersonUpdate(name=get_uuid())

        response = self.update_person(person_id, update.dict(), statuscode=status.HTTP_404_NOT_FOUND)
        assert response.json()["identifier"] == person_id

    def test_update_person_none_attributes(self):
        """
        빈 객체로 person 업데이트. 422 오류 반환
        """
        person = get_existing_person()
        self.update_person(person.person_id, {}, statuscode=status.HTTP_422_UNPROCESSABLE_ENTITY)

    def test_update_person_extra_attributes(self):
        """
        unknown 으로 person 업데이트. 422 오류 반환
        """
        person = get_existing_person()
        self.update_person(person.person_id, {"foo": "bar"}, statuscode=status.HTTP_422_UNPROCESSABLE_ENTITY)

    def test_timestamp_updated(self):
        iso_timestamp = "2020-04-01T00:00:00+00:00"
        expected_timestamp = int(datetime.fromisoformat(iso_timestamp).timestamp())
        person = get_existing_person()

        with freeze_time(iso_timestamp):
            update = PersonUpdate(name=get_uuid())
            PeopleRepository.update(person_id=person.person_id, update=update)

        read_response = self.get_person(person.person_id)
        read = PersonRead(**read_response.json())

        assert read.updated == expected_timestamp
        assert read.updated != read.created
        assert read.created == person.created
