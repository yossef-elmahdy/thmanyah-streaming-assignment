import os
from dotenv import load_dotenv

load_dotenv()

# Switch between running the code inside docker containers or on local machine
USE_DOCKER = False

KAFKA_HOST = 'kafka' if USE_DOCKER else 'localhost'
REDIS_HOST = 'redis' if USE_DOCKER else 'localhost'

# Kafka
KAFKA_BROKER_URL = os.getenv("KAFKA_BROKER_URL", f"kafka://{KAFKA_HOST}:9092")
KAFKA_ENGAGEMENT_TOPIC = os.getenv(
    "KAFKA_ENGAGEMENT_TOPIC", "thmanyah.public.engagement_events")
KAFKA_CONTENT_TOPIC = os.getenv(
    "KAFKA_CONTENT_TOPIC", "thmanyah.public.content")

# Redis
REDIS_HOST = os.getenv("REDIS_HOST", f"{REDIS_HOST}")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_AGGREGATOR_TIME_WINDOW = int(
    os.getenv("REDIS_AGGREGATOR_TIME_WINDOW", 600))
REDIS_AGGREGATOR_TOP_N = int(
    os.getenv("REDIS_AGGREGATOR_TOP_N", 5))

# External System (simulation)
EXTERNAL_API_URL = os.getenv(
    "EXTERNAL_API_URL", "http://external-system/api/ingest")

# Google BigQuery
BQ_CREDENTIALS_PATH = os.getenv(
    "BQ_CREDENTIALS_PATH", "/path/to/service-account.json")
BQ_PROJECT_ID = os.getenv("BQ_PROJECT_ID", "your-gcp-project-id")
BQ_DATASET_ID = os.getenv("BQ_DATASET_ID", "your_dataset")
BQ_TABLE_NAME = os.getenv("BQ_TABLE_NAME", "engagement_events")
BQ_TABLE_ID = f"{BQ_PROJECT_ID}.{BQ_DATASET_ID}.{BQ_TABLE_NAME}"
