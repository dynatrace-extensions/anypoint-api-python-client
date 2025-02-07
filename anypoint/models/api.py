from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from anypoint.api.api_manager import ApiManagerApi


class Asset:
    def __init__(self, raw_json, client: ApiManagerApi):
        self.id = raw_json.get("id")
        self.org_id = raw_json.get("organizationId")
        self.name = raw_json.get("name")
        self.exchange_asset_name = raw_json.get("exchangeAssetName")
        self.group_id = raw_json.get("groupId")
        self.asset_id = raw_json.get("assetId")
        self.apis: list[Api] = [Api(raw_data, client) for raw_data in raw_json.get("apis", [])]

    def __repr__(self):
        return f"Asset({self.id}, {self.asset_id})"


class Api:
    def __init__(self, raw_json, _client: ApiManagerApi):
        self.org_id = raw_json.get("organizationId")
        self.id = raw_json.get("id")
        self.instance_label = raw_json.get("instanceLabel")
        self.group_id = raw_json.get("groupId")
        self.asset_id = raw_json.get("assetId")
        self.asset_version = raw_json.get("assetVersion")
        self.product_version = raw_json.get("productVersion")
        self.description = raw_json.get("description")
        self.tags = raw_json.get("tags")
        self.order = raw_json.get("order")
        self.provider_id = raw_json.get("providerId")
        self.deprecated = raw_json.get("deprecated")
        self.last_active_date = raw_json.get("lastActiveDate")
        self.endpoint_uri = raw_json.get("endpointUri")
        self.environment_id = raw_json.get("environmentId")
        self.is_public = raw_json.get("isPublic")
        self.stage = raw_json.get("stage")
        self.technology = raw_json.get("technology")
        self.pinned = raw_json.get("pinned")
        self.active_contracts_count = raw_json.get("activeContractsCount")
        self.autodiscovery_instance_name = raw_json.get("autodiscoveryInstanceName")

    def __repr__(self):
        return f"Api({self.id}, {self.instance_label})"
