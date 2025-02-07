import logging

import requests

# Disable urllib warnings
from requests.adapters import HTTPAdapter
from urllib3 import Retry

requests.packages.urllib3.disable_warnings()

REQUEST_TIMEOUT = 60


class CustomRetry(Retry):
    def get_backoff_time(self):
        return self.backoff_factor


class HttpClient:
    def __init__(self, log: logging.Logger, proxies: dict | None = None, http_timeout: int = REQUEST_TIMEOUT):
        self._log = log
        self._proxies = proxies
        self._session = requests.Session()
        self.http_timeout = http_timeout
        self._session.mount(
            "https://",
            HTTPAdapter(
                max_retries=CustomRetry(
                    total=3,
                    backoff_factor=0.5,
                    status_forcelist=[429, 500, 502, 503, 504],
                    allowed_methods=["TRACE", "PUT", "DELETE", "OPTIONS", "HEAD", "GET", "POST"],
                    raise_on_status=False,
                )
            ),
        )

    def request(
        self,
        url: str,
        method: str = "GET",
        body: dict | None = None,
        headers: dict | None = None,
        parameters: dict | None = None,
        return_json=True,
    ) -> dict | requests.Response:
        try:
            self._log.debug(f"Making request {method} {url} {parameters if parameters else ''}")
            r = self._session.request(
                method,
                url,
                json=body,
                params=parameters,
                headers=headers,
                timeout=(self.http_timeout, self.http_timeout),
                proxies=self._proxies,
                verify=False,
            )
            self._log.debug(f"Received response {method} {url} {parameters if parameters else ''}: {r}")
            if r.status_code >= 400:
                error_message = f"Received a bad response: {method} {url}: {r}: {r.content}"
                raise Exception(error_message)
            # self._log.debug(f"Response: {r.json()}")
            return r.json() if return_json else r
        except Exception as e:
            self._log.exception(f"Could not make request {method} {url}: {repr(e)}")
            raise e
