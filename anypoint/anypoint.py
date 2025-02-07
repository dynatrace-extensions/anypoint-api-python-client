import logging

import requests

from anypoint.api.api_manager import ApiManagerApi
from anypoint.api.application import ApplicationApi
from anypoint.api.environment import EnvironmentApi
from anypoint.api.monitoring import MonitoringApi
from anypoint.api.mq import MQApi
from anypoint.api.organization import OrganizationApi
from anypoint.authentication import Authentication
from anypoint.http_client.client import HttpClient

_default_log = logging.getLogger(__name__)


class Anypoint:
    def __init__(
        self,
        authentication: Authentication,
        base_url: str = "https://anypoint.mulesoft.com",
        log: logging.Logger = _default_log,
        proxies: dict | None = None,
        http_timeout: int = 30,
    ):
        self._base_url = base_url
        self._authentication = authentication

        self.organizations = OrganizationApi(self, log)
        self.applications = ApplicationApi(self, log)
        self.environments = EnvironmentApi(self, log)
        self.monitoring = MonitoringApi(self, log)
        self.api_manager = ApiManagerApi(self, log)
        self.mq = MQApi(self, log)

        self._log = log
        self._access_token: str | None = None
        self._http_client = HttpClient(log, proxies, http_timeout=http_timeout)
        self._authentication.http_client = self._http_client

    def login(self):
        self._access_token = self._authentication.get_token(self._base_url)

    def me(self) -> dict:
        # TODO - Parse the response
        path = "/accounts/api/me"
        return self.request(path)

    def request(
        self,
        path: str,
        method: str = "GET",
        body: dict | None = None,
        headers: dict | None = None,
        parameters: dict | None = None,
        return_json=True,
    ) -> dict | requests.Response:
        url = f"{self._base_url}{path}"
        if not self._access_token and not url.endswith("/accounts/login"):
            self.login()
        if headers is None:
            headers = {}
        headers.update({"Authorization": f"Bearer {self._access_token}"})

        return self._http_client.request(url, method, body, headers, parameters, return_json)
