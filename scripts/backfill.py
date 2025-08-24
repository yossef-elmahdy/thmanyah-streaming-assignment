import json
import psycopg2
from kafka import KafkaProducer

# Postgres connection config
pg_conn = psycopg2.connect(
    host="localhost",         # or 'postgres' if running inside Docker
    port="5432",
    database="thmanyah_db",
    user="postgres",
    password="postgres"
)

# Kafka config
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

KAFKA_TOPIC = 'thmanyah.public.engagement_events'

# Date filter (inclusive): change as needed
START_DATE = '2025-01-01'
END_DATE = '2025-09-01'


def fetch_all_events(start_date, end_date):
    with pg_conn.cursor() as cursor:
        query = """
            SELECT * FROM public.engagement_events
            WHERE event_ts >= %s AND event_ts <= %s
            ORDER BY event_ts;
        """
        cursor.execute(query, (start_date, end_date))
        columns = [desc[0] for desc in cursor.description]
        for row in cursor.fetchall():
            yield dict(zip(columns, row))


def main():
    print(f"[Backfill] Starting replay from {START_DATE} to {END_DATE}")

    for event in fetch_all_events(START_DATE, END_DATE):
        # You can optionally transform here (e.g., add raw_payload: {})
        event['raw_payload'] = {}  # Optional, to match schema
        producer.send(KAFKA_TOPIC, event)
        print(f"[Backfill] Sent event: {event['content_id']}")

    producer.flush()
    print("[Backfill] All events sent.")


if __name__ == '__main__':
    main()
