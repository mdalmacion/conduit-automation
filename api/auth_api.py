from api.client import ApiClient
import requests


class AuthServiceException(Exception):
    """Base class for all AuthServices exception"""

class UserAlreadyExistsException(AuthServiceException):
    """Raised when a user already exists"""
    pass

class LoginFailedException(AuthServiceException):
    """Raised when user is unable to log in with the credentials"""
    pass

class AuthService:
    def __init__(self, client: ApiClient):
        self.client = client

    def extract_token(self, response) -> str:
        data = response.json()
        return data["user"]["token"]

    def register(self, email: str, username: str, password: str) -> requests.Response:
        response = self.client.post(
            "/users",
            json = {
                "user": {
                    "email": email,
                    "username": username,
                    "password": password,
                }
            }
        )

        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError:
            if response.status_code == 409:
                raise UserAlreadyExistsException(
                    "User with the same email/username already exists!"
                )
            else:
                raise AuthServiceException(
                    "AuthService encountered an error!"
                )

        token = self.extract_token(response)
        self.client.set_token(token)
        return response

    def login(self, email: str, password: str) -> requests.Response:
        response = self.client.post(
            "/users/login",
            json={
                "user": {
                    "email": email,
                    "password": password,
                }
            },
        )

        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as exc:
            if response.status_code == 401:
                raise LoginFailedException(
                    "Login failed. Check your credentials or if user is registered!"
                ) from exc
            raise AuthServiceException(
                "AuthService encountered an error!"
            ) from exc

        token = self.extract_token(response)
        self.client.set_token(token)
        return response