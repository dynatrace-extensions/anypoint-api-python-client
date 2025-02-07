import logging
from datetime import datetime
from typing import TYPE_CHECKING

from anypoint.models.destination import Destination, Queue

if TYPE_CHECKING:
    from anypoint import Anypoint

# Fri, 11 Jul 2015 08:49:37 GMT
DATE_FORMAT = "%a, %d %b %Y %H:%M:%S %Z"


class MQApi:
    def __init__(self, anypoint: "Anypoint", log: logging.Logger):
        self._client = anypoint
        self._log = log

    def get_destinations(self, organization_id: str, environment_id: str, region: str) -> list[Destination]:
        path = (
            f"/mq/admin/api/v1/organizations/{organization_id}/"
            f"environments/{environment_id}/regions/{region}/destinations"
        )
        data = self._client.request(path)
        return [Destination(d, self._client, organization_id, environment_id, region) for d in data]

    def get_queues(self, organization_id: str, environment_id: str, region: str, destinations: list[str]):
        path = (
            f"/mq/stats/api/v1/organizations/{organization_id}/"
            f"environments/{environment_id}/regions/{region}/queues"
        )
        params = {"destinationIds": ",".join(destinations) if destinations else None}
        return self._client.request(path, parameters=params)

    def get_queue(
        self,
        organization_id: str,
        environment_id: str,
        region: str,
        destination_id: str,
        start_date: datetime | None = None,
        end_date: datetime | None = None,
    ) -> Queue:
        path = (
            f"/mq/stats/api/v1/organizations/{organization_id}/"
            f"environments/{environment_id}/regions/{region}/queues/{destination_id}"
        )
        params = {
            "startDate": start_date.strftime(DATE_FORMAT) if start_date else None,
            "endDate": end_date.strftime(DATE_FORMAT) if end_date else None,
            "period": 86400,
        }
        data = self._client.request(path, parameters=params)
        return Queue(data)
