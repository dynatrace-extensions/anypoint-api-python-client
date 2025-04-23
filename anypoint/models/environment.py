from collections.abc import Generator
from typing import TYPE_CHECKING

from anypoint.api.v2.application import ApplicationApiV2
from anypoint.models.api import Asset
from anypoint.models.application import Application, ApplicationV2, ApplicationV2Details
from anypoint.models.destination import Destination, Queue

if TYPE_CHECKING:
    from anypoint import Anypoint


class Environment:
    def __init__(self, raw_json, client: "Anypoint"):
        self.id: str = raw_json.get("id")
        self.name: str = raw_json.get("name")
        self.is_production: bool = raw_json.get("isProduction")
        self.type: str = raw_json.get("type")
        self.client_id: str = raw_json.get("clientId")
        self.organization_id = raw_json.get("organizationId")
        self.applications: list[Application] = []
        self._v2 = ApplicationApiV2(client)

        self._data = raw_json
        self._client = client

    def __repr__(self):
        return f"Environment({self.name}, {self.id})"

    def v2_get_applications(self) -> Generator[Application, None, None]:
        return self._v2.get_applications(self.id)

    def get_applications(self) -> Generator[Application, None, None]:
        return self._client.applications.get_applications(self.id)

    def get_applications_v2(self) -> Generator[ApplicationV2, None, None]:
        return self._client.applications.get_applications_v2(self.organization_id, self.id)

    def get_application_v2(self, deployment_id: str) -> ApplicationV2Details:
        return self._client.applications.get_application_v2(self.organization_id, self.id, deployment_id)

    def get_apis(self, limit: int = 100, offset: int = 0, paginate: bool = False) -> Generator[Asset, None, None]:
        if not paginate:
            return self._client.api_manager.get_apis(self.organization_id, self.id, limit=limit, offset=offset)
        else:
            while True:
                assets = self._client.api_manager.get_apis(self.organization_id, self.id, limit=limit, offset=offset)
                if not assets:
                    break
                for asset in assets:
                    yield asset
                offset += limit

    def get_organization(self):
        return self._client.organizations.get_environment_organization(self.id)

    def get_mq_queues(self, region_id: str, destinations: list[str] = None):
        return self._client.mq.get_queues(self.organization_id, self.id, region_id, destinations)

    def get_mq_queue(self, region_id: str, destination_id: str) -> Queue:
        return self._client.mq.get_queue(self.organization_id, self.id, region_id, destination_id)

    def get_mq_destinations(self, region_id: str) -> list[Destination]:
        return self._client.mq.get_destinations(self.organization_id, self.id, region_id)
