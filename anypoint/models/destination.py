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


class Queue:
    def __init__(self, raw_json):
        self.destination: str = raw_json.get("destination")
        # Grab the value of the first item in the list
        self.messages = raw_json.get("messages", [{}])[0].get("value")
        self.inflight_messages = raw_json.get("inflightMessages", [{}])[0].get("value")
        self.messages_visible = raw_json.get("messagesVisible", [{}])[0].get("value")
        self.messages_sent = raw_json.get("messagesSent", [{}])[0].get("value")
        self.messages_received = raw_json.get("messagesReceived", [{}])[0].get("value")
        self.messages_acked = raw_json.get("messagesAcked", [{}])[0].get("value")

    def __repr__(self):
        return f"Queue({self.destination}, {self.messages=}, {self.inflight_messages=})"
