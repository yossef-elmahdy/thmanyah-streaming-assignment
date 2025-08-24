import uuid
import random
import psycopg2
from datetime import datetime, timedelta
from faker import Faker
import json


def main():
    print("Generating mock data...")

    fake = Faker()

    conn = psycopg2.connect(
        host="localhost",
        port=5432,
        dbname="thmanyah_db",
        user="postgres",
        password="postgres"
    )
    cursor = conn.cursor()

    # Constants (Enums for random choice)
    CONTENT_TYPES = ['podcast', 'newsletter', 'video']
    EVENT_TYPES = ['play', 'pause', 'finish', 'click']
    DEVICES = ['ios', 'android', 'web-chrome', 'web-safari']

    NUM_CONTENT = 10
    NUM_EVENTS = 50

    # Insert Content
    content_ids = []
    for _ in range(NUM_CONTENT):
        cid = uuid.uuid4()
        content_ids.append(cid)
        cursor.execute("""
            INSERT INTO content (id, slug, title, content_type, length_seconds, publish_ts)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (id) DO NOTHING;
        """, (
            str(cid),
            fake.slug(),
            fake.sentence(nb_words=5),
            random.choice(CONTENT_TYPES),
            random.randint(30, 900),  # 0.5 to 15 minutes
            datetime.now() - timedelta(days=random.randint(0, 30))
        ))

    # Insert Engagement Events
    for _ in range(NUM_EVENTS):
        cid = random.choice(content_ids)
        uid = uuid.uuid4()
        event_type = random.choice(EVENT_TYPES)
        duration_ms = random.randint(1000, 300000) if event_type in [
            'play', 'finish'] else None
        payload = {
            "ip": fake.ipv4(),
            "user_agent": fake.user_agent()
        }

        cursor.execute("""
            INSERT INTO engagement_events (content_id, user_id, event_type, event_ts, duration_ms, device, raw_payload)
            VALUES (%s, %s, %s, %s, %s, %s, %s);
        """, (
            str(cid),
            str(uid),
            event_type,
            datetime.now(),
            duration_ms,
            random.choice(DEVICES),
            json.dumps(payload)
        ))

    conn.commit()
    cursor.close()
    conn.close()

    print(
        f"✅ Inserted {NUM_CONTENT} content records and {NUM_EVENTS} engagement events.")


if __name__ == "__main__":
    main()
