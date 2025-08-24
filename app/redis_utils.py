import time
import redis
from collections import Counter
from app.config import (
    REDIS_HOST,
    REDIS_PORT,
    REDIS_AGGREGATOR_TIME_WINDOW,
    REDIS_AGGREGATOR_TOP_N,
)


redis_client = redis.Redis(
    host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)


def set_content(content_id, content_type, length_seconds):
    key = f"content:{content_id}"
    redis_client.hset(key, mapping={
        "content_type": content_type,
        "length_seconds": length_seconds
    })


def get_content(content_id):
    return redis_client.hgetall(f"content:{content_id}")


def add_engagement_score(content_id, score):
    try:
        redis_client.zadd("engagement_scores", {
                          f"engagement:{content_id}": score})
    except Exception as e:
        print(
            f"[Redis] Error adding engagement score for content {content_id}: {e}")


def update_engagement_stream(content_id):
    try:
        redis_client.zadd("engagement_stream", {content_id: int(time.time())})
    except Exception as e:
        print(f"[Redis] Error updating stream for content {content_id}: {e}")


def get_top_content_last_n_minutes(window_seconds=REDIS_AGGREGATOR_TIME_WINDOW, top_n=REDIS_AGGREGATOR_TOP_N):
    now = int(time.time())
    min_score = now - window_seconds
    try:
        content_ids = redis_client.zrangebyscore(
            "engagement_stream", min_score, now)
        counter = Counter(content_ids)
        top = counter.most_common(top_n)
        print(
            f"Top Content in Last {int(REDIS_AGGREGATOR_TIME_WINDOW/60)} Minutes:")

        for content_id, count in top:
            print(f"{content_id} - {count} interactions")
        return top
    except Exception as e:
        print(f"[Redis] Aggregation error: {e}")
        return []


def store_top_content(top_content):
    try:
        redis_client.delete(
            f"top:content:last_{int(REDIS_AGGREGATOR_TIME_WINDOW/60)}_minutes")
        for cid, count in top_content:
            redis_client.hset(
                f"top:content:last_{int(REDIS_AGGREGATOR_TIME_WINDOW/60)}_minutes", cid, count)
        print(
            f"[Aggregator] Top {REDIS_AGGREGATOR_TOP_N} content updated in Redis:", top_content)
    except Exception as e:
        print(f"[Aggregator] Error during aggregation: {e}")
