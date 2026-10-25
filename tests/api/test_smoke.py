import pytest
from api.client import ApiClient
from api.auth_api import AuthService
from api.auth_api import LoginFailedException

def test_login_unregistered():
    c = ApiClient('https://api.realworld.show/api')
    auth_service = AuthService(c)
    with pytest.raises(LoginFailedException):
        auth_service.login('test@root.com', 'password')


def test_register_new_user():
    c = ApiClient('https://api.realworld.show/api')
    auth_service = AuthService(c)
    response = auth_service.register('test123@testemail.com','testuser',  'password')

    assert response.status_code == 201, 'Failed to register new user'

def test_login_registered():
    c = ApiClient('https://api.realworld.show/api')
    auth_service = AuthService(c)
    response = auth_service.login('test123@testemail.com', 'password')

    assert response.status_code == 200, 'Unable to login'



