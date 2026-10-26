import redis

from app.config import settings


redis_client = redis.from_url(
    settings.redis_url,
    decode_responses=True
)


def check_redis_connection() -> bool:
    try:
        return bool(redis_client.ping())
    except Exception:
        return False


def get_cached_statistics():
    try:
        return redis_client.get(
            "civicpulse:statistics"
        )
    except Exception:
        return None


def set_cached_statistics(data: str):
    try:
        redis_client.setex(
            "civicpulse:statistics",
            30,
            data
        )
    except Exception:
        pass


def invalidate_statistics_cache():
    try:
        redis_client.delete(
            "civicpulse:statistics"
        )
    except Exception:
        pass