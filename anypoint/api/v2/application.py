from collections.abc import Generator
from typing import TYPE_CHECKING

from anypoint.models.application import Application, ApiVersion

if TYPE_CHECKING:
    from anypoint import Anypoint


class ApplicationApiV2:
    def __init__(self, anypoint: "Anypoint"):
        self._client = anypoint

    def get_applications(self, environment_id: str) -> Generator[Application, None, None]:
        path = "/cloudhub/api//v2/applications"
        headers = {"X-ANYPNT-ENV-ID": environment_id}
        data = self._client.request(path, headers=headers)

        for app in data:
            app["environment_id"] = environment_id
            yield Application(app, self, ApiVersion.V2)
