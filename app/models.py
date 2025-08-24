import faust


class EngagementEvent(faust.Record, serializer='json'):
    content_id: str
    user_id: str
    event_type: str
    event_ts: str
    duration_ms: int
    device: str
    raw_payload: dict


class ContentUpdate(faust.Record, serializer='json'):
    id: str
    content_type: str
    length_seconds: int
