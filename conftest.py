import pytest
from config import BASE_URL, API_USERNAME, API_PASSWORD
from api.client import ApiClient
from api.auth_api import AuthService
from api.articles_api import ArticleService

@pytest.fixture
def auth_service():
    # Fresh client with no token for every auth test
    return AuthService(ApiClient(base_url=BASE_URL))

@pytest.fixture(scope="session")
def authenticated_client():
    # Its own client, so its token never reaches the auth tests
    client = ApiClient(base_url=BASE_URL)
    AuthService(client).login(API_USERNAME, API_PASSWORD)
    return client

@pytest.fixture
def articles_service(authenticated_client):
    return ArticleService(authenticated_client)