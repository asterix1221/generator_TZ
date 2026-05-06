import json
from typing import Optional

import redis.asyncio as aioredis

from app.core.config import get_settings

settings = get_settings()

_redis_pool: Optional[aioredis.Redis] = None


async def get_redis() -> aioredis.Redis:
    global _redis_pool
    if _redis_pool is None:
        _redis_pool = aioredis.from_url(
            settings.REDIS_URL,
            decode_responses=True,
            max_connections=20,
        )
    return _redis_pool


async def close_redis() -> None:
    global _redis_pool
    if _redis_pool is not None:
        await _redis_pool.close()
        _redis_pool = None


async def cache_template(
    template_type: str,
    complexity: int,
    data: dict,
    ttl: int = 3600,
) -> None:
    """Cache a template in Redis with TTL."""
    redis = await get_redis()
    key = f"template:{template_type}:{complexity}"
    await redis.setex(key, ttl, json.dumps(data, default=str))


async def get_cached_template(template_type: str, complexity: int) -> Optional[dict]:
    """Get a cached template from Redis."""
    redis = await get_redis()
    key = f"template:{template_type}:{complexity}"
    data = await redis.get(key)
    if data:
        return json.loads(data)
    return None


async def check_rate_limit(
    identifier: str,
    max_requests: int = 20,
    window: int = 60,
) -> bool:
    """
    Rate limiting using Redis.

    Fail-open behavior for tests/CI:
    if Redis/connection fails (including event-loop related issues),
    we return True (allow request) instead of raising.
    """
    try:
        redis = await get_redis()
        key = f"ratelimit:{identifier}"

        current = await redis.get(key)
        if current is None:
            await redis.setex(key, window, 1)
            return True

        count = int(current)
        if count >= max_requests:
            return False

        await redis.incr(key)
        return True
    except Exception:
        return True


async def get_rate_limit_ttl(identifier: str) -> int:
    """Get remaining TTL for rate limit window (fail-safe)."""
    try:
        redis = await get_redis()
        key = f"ratelimit:{identifier}"
        ttl = await redis.ttl(key)
        if ttl is None:
            return 0
        return max(0, int(ttl))
    except Exception:
        return 0
