"""Illustrative Branch B: a Redis-backed FastAPI limiter.

HTTP response paths are checked with a fake allow/deny result.
The shared-counter path requires the ``redis`` and ``fastapi`` packages
plus a Redis server at ``localhost:6379``; no live Redis or load test
is claimed by the response checks.
"""

import time

import redis.asyncio as redis
from fastapi import Request
from fastapi.responses import JSONResponse

RATE_LIMIT_SCRIPT = """
local key = KEYS[1]
local limit = tonumber(ARGV[1])
local window = tonumber(ARGV[2])
local now = tonumber(ARGV[3])

redis.call(
    "ZREMRANGEBYSCORE",
    key,
    0,
    now - window
)
local count = redis.call("ZCARD", key)
if count >= limit then
    return 0
end
redis.call("ZADD", key, now, now)
redis.call("EXPIRE", key, window)
return 1
"""                                   # A

_redis = redis.from_url("redis://localhost:6379")


async def check_rate_limit(
    user_id: str,
    max_requests: int = 100,
    window_seconds: int = 60,
) -> bool:
    now = time.time()
    result = await _redis.eval(       # B
        RATE_LIMIT_SCRIPT,
        1,
        f"rate:{user_id}",
        max_requests,
        window_seconds,
        now,
    )
    return bool(result)


async def rate_limit_middleware(
    request: Request,
    call_next,
):
    user = request.state.user_id      # C
    allowed = await check_rate_limit(user)
    if not allowed:
        return JSONResponse(
            status_code=429,
            content={"detail": "Rate limit exceeded"},
        )
    return await call_next(request)   # D
