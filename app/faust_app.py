import faust
import json
from app.models import EngagementEvent, ContentUpdate
from app.config import (
    KAFKA_BROKER_URL,
    KAFKA_ENGAGEMENT_TOPIC,
    KAFKA_CONTENT_TOPIC,
    EXTERNAL_API_URL
)
from app.redis_utils import set_content, add_engagement_score, update_engagement_stream, get_top_content_last_n_minutes, store_top_content
from app.bigquery_utils import insert_to_bigquery
from app.enrichment import enrich_event


app = faust.App(
    'thmanyah-streaming-application',
    broker=KAFKA_BROKER_URL,
    value_serializer='raw',
)


event_topic = app.topic(KAFKA_ENGAGEMENT_TOPIC, value_type=EngagementEvent)
content_topic = app.topic(KAFKA_CONTENT_TOPIC, value_type=ContentUpdate)


@app.agent(content_topic)
async def sync_content_table(contents):
    async for content in contents:
        try:
            set_content(content.id, content.content_type,
                        content.length_seconds)
            print(f"[Redis] Synced content {content.id}")
        except Exception as e:
            print(f"[Redis] Error syncing content {content.id}: {e}")


@app.agent(event_topic)
async def process(events):
    async for event in events:
        enriched = enrich_event(event)
        if enriched:
            add_engagement_score(
                event.content_id, enriched["engagement_pct"] or 0)
            update_engagement_stream(event.content_id)
            top = get_top_content_last_n_minutes()
            store_top_content(top)

            print(f"[External System] POST to Simulated API: {EXTERNAL_API_URL}", json.dumps(
                enriched))
            # insert_to_bigquery(enriched) # Tested before but stream insert is not allowed For free-tier user


@app.timer(interval=60.0)
async def periodic_aggregation():
    print("[Timer] Running periodic top content aggregation")
    top = get_top_content_last_n_minutes()
    store_top_content(top)
