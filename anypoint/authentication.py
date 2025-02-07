import abc
from abc import ABC

from anypoint.http_client.client import HttpClient


class Authentication(ABC):
    def __init__(self):
        self._http_client = None

    @abc.abstractmethod
    def get_token(self, url: str) -> str:
        raise NotImplementedError

    @property
    def http_client(self) -> HttpClient:
        return self._http_client

    @http_client.setter
    def http_client(self, http_client: HttpClient):
        self._http_client = http_client


class Basic(Authentication):
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password
        super().__init__()

    def get_token(self, url: str) -> str:
        path = f"{url}/accounts/login"
        r = self._http_client.request(
            path, "POST", body={"username": self.username, "password": self.password}
        )
        return r.get("access_token")


class OAuth2(Authentication):
    def __init__(self, client_id: str, client_secret: str):
        self.client_id = client_id
        self.client_secret = client_secret
        super().__init__()

    def get_token(self, url: str) -> str:
        path = f"{url}/accounts/api/v2/oauth2/token"
        body = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": "client_credentials",
        }
        headers = {"Content-Type": "application/json"}
        r = self._http_client.request(path, "POST", body=body, headers=headers)
        return r.get("access_token")
