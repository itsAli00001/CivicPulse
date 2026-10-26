
import redis

from app.config import settings


redis_client = redis.from_url(
    settings.redis_url,
    decode_responses=True,
    socket_connect_timeout=3,
    socket_timeout=3,
)


def check_redis_connection() -> bool:
    try:
        return bool(redis_client.ping())
    except redis.RedisError:
        return False


def get_cached_statistics():
    try:
        return redis_client.get("civicpulse:statistics")
    except redis.RedisError:
        return None


def set_cached_statistics(data: str):
    try:
        redis_client.set(
            "civicpulse:statistics",
            data,
            ex=30,
        )
    except redis.RedisError:
        pass


def invalidate_statistics_cache():
    try:
        redis_client.delete("civicpulse:statistics")
    except redis.RedisError:
        pass


def check_rate_limit(
    client_id: str,
    limit: int = 10,
    window_seconds: int = 60,
) -> tuple[bool, int]:
    key = f"civicpulse:rate-limit:{client_id}"

    try:
        count = redis_client.incr(key)

        if count == 1:
            redis_client.expire(key, window_seconds)

        remaining = max(0, limit - count)

        if count > limit:
            ttl = redis_client.ttl(key)
            retry_after = max(1, ttl)
            return False, retry_after

        return True, remaining

    except redis.RedisError:
        # Keep the API available if Redis is temporarily unavailable.
        return True, limit
