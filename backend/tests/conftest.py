from pytest import fixture
from fastapi.testclient import TestClient

from dating.users.crud import USERS_DB
from dating.main.api import app


@fixture(scope="function", autouse=True)
def clear_db():
    USERS_DB.clear()


@fixture()
def client() -> TestClient:
    return TestClient(app)
