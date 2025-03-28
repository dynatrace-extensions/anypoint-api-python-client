from __future__ import annotations

import logging
import typing

from anypoint.models.api import Asset

if typing.TYPE_CHECKING:
    from anypoint import Anypoint


class ApiManagerApi:
    def __init__(self, client: Anypoint, log: logging.Logger):
        self._client = client
        self._log = log

    def get_apis(self, organization_id: str, environment_id: str, limit: int = 100, offset: int = 0) -> list[Asset]:
        path = f"/apimanager/api/v1/organizations/{organization_id}/environments/{environment_id}/apis"
        assets = self._client.request(path, parameters={
            "limit": limit,
            "offset": offset
        }).get("assets", [])
        return [Asset(asset, self) for asset in assets]
