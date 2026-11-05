from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from anypoint import Anypoint


class Destination:
    def __init__(self, raw_json, client: Anypoint, organization_id: str, environment_id: str, region_id: str):
        self.organization_id = organization_id
        self.environment_id = environment_id
        self.region_id = region_id

        self.encrypted: bool = raw_json.get("encrypted")
        self.type: str = raw_json.get("type")
        self.queue_id: str = raw_json.get("queueId")
        self.dead_letter_sources: str = raw_json.get("deadLetterSources")
        self.fifo: bool = raw_json.get("fifo")
        self.default_ttl: int = raw_json.get("defaultTtl")
        self.default_lock_ttl: int = raw_json.get("defaultLockTtl")
        self.default_delivery_delay: int = raw_json.get("defaultDeliveryDelay")
        self.max_deliveries: int = raw_json.get("maxDeliveries")
        self.dead_letter_queue_id: str = raw_json.get("deadLetterQueueId")

        self._data = raw_json
        self._client = client

    def __repr__(self):
        return f"Destination({self.queue_id}, {self.type})"

    def get_queue(self, start_date: datetime | None = None, end_date: datetime | None = None):
        return self._client.mq.get_queue(
            self.organization_id, self.environment_id, self.region_id, self.queue_id, start_date, end_date
        )


def _first_value(raw_json: dict, key: str) -> int | float | None:
    """Value of the first datapoint of a Stats API series, or None if there is none.

    A series is a list of ``{"date": ..., "value": ...}`` items, but it can be
    missing, ``null`` or an empty list (no datapoints in the requested window).
    """
    series = raw_json.get(key)
    if not isinstance(series, list) or not series or not isinstance(series[0], dict):
        return None
    return series[0].get("value")


class Queue:
    def __init__(self, raw_json):
        self.destination: str = raw_json.get("destination")
        # Value of the first datapoint of each series, None when the series has no datapoints
        self.messages = _first_value(raw_json, "messages")
        self.inflight_messages = _first_value(raw_json, "inflightMessages")
        self.messages_visible = _first_value(raw_json, "messagesVisible")
        self.messages_sent = _first_value(raw_json, "messagesSent")
        self.messages_received = _first_value(raw_json, "messagesReceived")
        self.messages_acked = _first_value(raw_json, "messagesAcked")

    def __repr__(self):
        return f"Queue({self.destination}, {self.messages=}, {self.inflight_messages=})"
