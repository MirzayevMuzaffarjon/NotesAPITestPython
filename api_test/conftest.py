import pytest
from api_test.clients.base_client import BaseClient
from api_test.utils.assertions import Assertions
from api_test.config import Config
from api_test.data.users import UsersData


@pytest.fixture(scope="session")
def config():
    """Create configuration instance."""
    return Config()


@pytest.fixture(scope="session")
def client(config):
    """Create base HTTP client instance.
    
    Args:
        config: Configuration fixture.
        
    Returns:
        BaseClient instance.
    """
    return BaseClient(base_url=config.base_url)


@pytest.fixture(scope="session")
def assertions():
    """Create assertions utility instance."""
    return Assertions()


@pytest.fixture(scope="session")
def users_data():
    """Create test data generator instance."""
    return UsersData()