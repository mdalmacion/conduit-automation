import pytest
from api.auth_api import LoginFailedException, UserAlreadyExistsException

def test_login_unregistered(auth_service):
    with pytest.raises(LoginFailedException):
        auth_service.login('test@root.com', 'password')

def test_register_new_user(auth_service):
    response = auth_service.register('test123@testemail.com','testuser',  'password')
    assert response.status_code == 201, 'Failed to register new user'

def test_login_registered(auth_service):
    response = auth_service.login('test123@testemail.com', 'password')
    assert response.status_code == 200, 'Unable to login'

def test_already_registered(auth_service):
    response_1 = auth_service.register('test123@testemail.com', 'testuser', 'password')
    with pytest.raises(UserAlreadyExistsException):
        auth_service.register('test123@testemail.com', 'testuser', 'password')

