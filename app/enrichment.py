from app.redis_utils import get_content


def enrich_event(event):
    content = get_content(event.content_id)
    if not content:
        print(f"[Redis] Missing content for {event.content_id}")
        return None

    try:
        length = int(content.get("length_seconds", 0))
        engagement_seconds = round(event.duration_ms / 1000.0,
                                   2) if event.duration_ms else None
        engagement_pct = round(engagement_seconds /
                               length, 2) if length else None

        return {
            "content_id": event.content_id,
            "user_id": event.user_id,
            "event_type": event.event_type,
            "event_ts": event.event_ts,
            "device": event.device,
            "content_type": content.get("content_type"),
            "length_seconds": length,
            "engagement_seconds": engagement_seconds,
            "engagement_pct": engagement_pct,
        }
    except Exception as e:
        print(
            f"[Enrichment] Error for Event with Content ID {event.content_id}: {e}")
        return None
