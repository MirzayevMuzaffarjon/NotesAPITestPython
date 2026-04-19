import pytest
from api_test.clients.base_client import BaseClient
from api_test.utils.assertions import Assertions
from api_test.config import Config
from api_test.data.users import UsersData


@pytest.fixture(scope="session")
def client():
    return BaseClient()

@pytest.fixture(scope="session")
def assertions():
    return Assertions()

@pytest.fixture(scope="session")
def config():
    return Config()

@pytest.fixture(scope="session")
def users_data():
    return UsersData()