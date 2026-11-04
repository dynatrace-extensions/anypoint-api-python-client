"""Tests for the MQ ``Queue`` model's parsing of Stats API responses.

The Stats API returns each series as a list of ``{"date": ..., "value": ...}``
datapoints. A series can come back as an empty list (no datapoints in the
requested window, e.g. an idle queue) or as ``null``. Those cases must not
raise, otherwise callers can't get any stats for the queue.
"""

from anypoint.models.destination import Queue

SERIES_KEYS = {
    "messages": "messages",
    "inflightMessages": "inflight_messages",
    "messagesVisible": "messages_visible",
    "messagesSent": "messages_sent",
    "messagesReceived": "messages_received",
    "messagesAcked": "messages_acked",
}

DATE = "2023-03-01T16:34:00.000+00:00"


def _payload(**series):
    """Build a Stats API response with every series populated, overriding some."""
    data = {"destination": "Q"}
    for i, key in enumerate(SERIES_KEYS):
        data[key] = [{"date": DATE, "value": i + 1}]
    data.update(series)
    return data


def test_queue_normal_payload():
    raw = {
        "destination": "CUSTOMER-CREATE-SFMC-Q",
        "messages": [{"date": DATE, "value": 144}],
        "inflightMessages": [{"date": DATE, "value": 0}],
        "messagesVisible": [{"date": DATE, "value": 144}],
        "messagesSent": [{"date": DATE, "value": 57}],
        "messagesReceived": [{"date": DATE, "value": 0}],
        "messagesAcked": [{"date": DATE, "value": 0}],
    }

    queue = Queue(raw)

    assert queue.destination == "CUSTOMER-CREATE-SFMC-Q"
    assert queue.messages == 144
    assert queue.inflight_messages == 0
    assert queue.messages_visible == 144
    assert queue.messages_sent == 57
    assert queue.messages_received == 0
    assert queue.messages_acked == 0


def test_queue_empty_series_does_not_raise():
    queue = Queue({"destination": "Q", **{key: [] for key in SERIES_KEYS}})

    for attr in SERIES_KEYS.values():
        assert getattr(queue, attr) is None, attr


def test_queue_empty_series_only_affects_that_series():
    queue = Queue(_payload(messages=[]))

    assert queue.messages is None
    assert queue.inflight_messages == 2
    assert queue.messages_acked == 6


def test_queue_null_series_does_not_raise():
    queue = Queue({"destination": "Q", **dict.fromkeys(SERIES_KEYS)})

    for attr in SERIES_KEYS.values():
        assert getattr(queue, attr) is None, attr


def test_queue_missing_series():
    queue = Queue({"destination": "Q"})

    for attr in SERIES_KEYS.values():
        assert getattr(queue, attr) is None, attr


def test_queue_item_without_value():
    queue = Queue(_payload(messages=[{"date": DATE}], inflightMessages=[{}]))

    assert queue.messages is None
    assert queue.inflight_messages is None
    assert queue.messages_visible == 3
