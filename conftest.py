import pytest

from config import BASE_URL
from api.client import ApiClient
from api.auth_api import AuthService
from api.articles_api import ArticleService


BASE_URL = "https://api.realworld.show/api"

@pytest.fixture(scope="session")
def api_client():
    return ApiClient(base_url=BASE_URL)

@pytest.fixture(scope="session")
def auth_service(api_client):
    return AuthService(api_client)

@pytest.fixture(scope="session")
def authenticated_client(api_client, auth_service):
    auth_service.login('test123@testemail.com', 'password')
    return api_client

@pytest.fixture
def articles_service(authenticated_client):
    return ArticleService(authenticated_client)