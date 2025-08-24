import json
import redis
from pyflink.common import SimpleStringSchema, Types
from pyflink.datastream import StreamExecutionEnvironment, MapFunction
from pyflink.datastream.connectors import FlinkKafkaConsumer

# External System URL (placeholder)
EXTERNAL_URL = "http://external-system/api/ingest"

# Mock content lookup (in real system, use broadcast state or external store)
content_lookup = {
    "11111111-1111-1111-1111-111111111111": {
        "content_type": "podcast",
        "length_seconds": 200
    }
    # Add more as needed
}


def enrich_event(event, content_lookup):
    try:
        content = content_lookup.get(event['content_id'])
        if not content:
            return None  # Skip if content not found

        length_seconds = content.get('length_seconds')
        duration_ms = event.get('duration_ms')

        engagement_seconds = round(duration_ms / 1000.0, 2) if duration_ms else None
        engagement_pct = round(engagement_seconds / length_seconds, 2) if (engagement_seconds and length_seconds) else None

        enriched = {
            **event,
            "content_type": content.get("content_type"),
            "length_seconds": length_seconds,
            "engagement_seconds": engagement_seconds,
            "engagement_pct": engagement_pct
        }
        return enriched
    except Exception as e:
        print(f"Enrichment error: {e}")
        return None


class FanoutSink(MapFunction):
    def open(self, runtime_context):
        self.redis_client = redis.Redis(host='redis', port=6379, decode_responses=True)

    def map(self, enriched_event):
        json_str = json.dumps(enriched_event)

        # 1. Redis
        try:
            key = f"engagement:{enriched_event['content_id']}"
            # self.redis_client.zadd("engagement_scores", {key: enriched_event['engagement_pct'] or 0})
        except Exception as e:
            print(f"Redis error: {e}")

        # 2. External system (commented for now)
        # try:
        #     requests.post(EXTERNAL_URL, json=enriched_event, timeout=2)
        # except Exception as e:
        #     print(f"External system error: {e}")

        # 3. BigQuery simulation
        print(f"[BigQuery] {json_str}")
        return enriched_event


def main():
    env = StreamExecutionEnvironment.get_execution_environment()
    env.set_parallelism(1)

    kafka_props = {
        'bootstrap.servers': 'kafka:9092',
        'group.id': 'flink-consumer',
        'auto.offset.reset': 'earliest'
    }

    kafka_source = FlinkKafkaConsumer(
        topics='thmanyah.public.engagement_events',
        deserialization_schema=SimpleStringSchema(),
        properties=kafka_props
    )

    ds = env.add_source(kafka_source) \
            .map(lambda x: json.loads(x), output_type=Types.MAP(Types.STRING(), Types.STRING())) \
            .map(lambda event: enrich_event(event, content_lookup)) \
            .filter(lambda x: x is not None) \
            .map(FanoutSink(), output_type=Types.MAP(Types.STRING(), Types.STRING()))

    env.execute("Thmanyah Engagement Event Pipeline")


if __name__ == '__main__':
    main()
