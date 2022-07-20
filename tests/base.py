from multiprocessing import Process

import httpx
from wait4it import get_free_port, wait_for

from src import run
from src.database import collection
from src.settings import api_settings


__all__ = ("BaseTest", )


class BaseTest:
    api_process: Process
    api_url: str

    @classmethod
    def setup_class(cls):
        api_port = api_settings.port = get_free_port()
        # api_port = get_free_port()
        # print("api_port ====> ", api_port)
        cls.api_url = f"http://localhost:{api_port}"
        # print("api_settings.port ====> ", api_settings.port)
        cls.api_process = Process(target=run, daemon=True)
        cls.api_process.start()
        wait_for(port=api_port)

    @classmethod
    def teardown_class(cls):
        cls.api_process.terminate()

    @classmethod
    def teardown_method(cls):
        collection.delete_many({})

    # API Methods #

    def get_person(self, person_id: str, statuscode: int = 200):
        r = httpx.get(f"{self.api_url}/people/{person_id}")
        assert r.status_code == statuscode, r.text
        return r

    def create_person(self, create: dict, statuscode: int = 201):
        r = httpx.post(f"{self.api_url}/people", json=create)
        assert r.status_code == statuscode, r.text
        return r

    def list_people(self, statuscode: int = 200):
        r = httpx.get(f"{self.api_url}/people")
        assert r.status_code == statuscode, r.text
        return r

    def update_person(self, person_id: str, update: dict, statuscode: int = 204):
        r = httpx.patch(f"{self.api_url}/people/{person_id}", json=update)
        assert r.status_code == statuscode, r.text
        return r

    def delete_person(self, person_id: str, statuscode: int = 204):
        r = httpx.delete(f"{self.api_url}/people/{person_id}")
        assert r.status_code == statuscode, r.text
        return r


