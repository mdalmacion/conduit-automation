import requests
from typing import Any, Dict, Optional

class ApiClient:

    def __init__(self, base_url: str, timeout : int = 10) -> None:
        self.base_url = base_url
        self.timeout = timeout

        self.session = requests.Session()
        self.session.headers['Content-Type'] = 'application/json'
        self.session.headers['Accept']='application/json'

    def set_token(self, token: str) -> None:
        self.session.headers["Authorization"] = f"Token {token}"

    def clear_token(self) -> None:
        self.session.headers.pop("Authorization", None)

    def _build_url(self, endpoint: str) -> str:
        end = endpoint.lstrip('/')
        base = self.base_url.rstrip('/')
        return f"{base}/{end}"

    def _request(self, method: str, endpoint: str, **kwargs: Any) -> requests.Response:
        url = self._build_url(endpoint)
        kwargs.setdefault("timeout",self.timeout)
        return self.session.request(method, url, **kwargs)

    # _request wrappers
    def get(self, endpoint: str, **kwargs: Any) -> requests.Response:
        return self._request("GET", endpoint, **kwargs)

    def post(self, endpoint: str, **kwargs: Any) -> requests.Response:
        return self._request("POST", endpoint, **kwargs)

    def put(self, endpoint: str, **kwargs: Any) -> requests.Response:
        return self._request("PUT", endpoint, **kwargs)

    def delete(self, endpoint: str, **kwargs: Any) -> requests.Response:
        return self._request("DELETE", endpoint, **kwargs)
