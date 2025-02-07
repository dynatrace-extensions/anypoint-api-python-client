import logging
from collections.abc import Generator
from typing import TYPE_CHECKING

from anypoint.models.environment import Environment
from anypoint.models.organization import Organization
from anypoint.models.private_space import Connection, PrivateSpace

if TYPE_CHECKING:
    from anypoint import Anypoint


class OrganizationApi:
    def __init__(self, client: "Anypoint", log: logging.Logger):
        self._client = client
        self._log = log

    def get_organization(self, org_id: str | None = None) -> Organization:
        if org_id is None:
            data = self._client.me()
            data = data.get("user", {}).get("organization", {})
        else:
            path = f"/accounts/api/organizations/{org_id}"
            data = self._client.request(path)
        return Organization(data, self)

    def get_environments(self, organization_id: str) -> Generator[Environment, None, None]:
        path = f"/accounts/api/organizations/{organization_id}/environments"
        data = self._client.request(path)
        for env in data.get("data", []):
            env["organization_id"] = organization_id
            yield Environment(env, self._client)

    def get_environment_organization(self, environment_id: str) -> Organization:
        path = "/cloudhub/api/organization"
        headers = {"X-ANYPNT-ENV-ID": environment_id}
        data = self._client.request(path, headers=headers)
        return Organization(data, self)

    def get_private_spaces(self, organization_id: str) -> list[PrivateSpace]:
        path = f"/runtimefabric/api/organizations/{organization_id}/privatespaces"
        data = self._client.request(path)
        content = data.get("content", [])
        return [PrivateSpace(x, self._client) for x in content]

    def get_private_space_connections(self, organization_id: str, private_space_id: str) -> list[Connection]:
        path = (
            f"/runtimefabric/api/organizations/{organization_id}/privatespaces/{private_space_id}/connections"
        )
        data = self._client.request(path)
        return [Connection(x) for x in data]
