import time
import redis.asyncio as redis
from fastapi import HTTPException, Request

_redis = redis.from_url(              #A
    "redis://localhost:6379"
)

RATE_LIMIT_SCRIPT = """               #B
local key = KEYS[1]
local limit = tonumber(ARGV[1])
local window = tonumber(ARGV[2])
local now = tonumber(ARGV[3])
redis.call('ZREMRANGEBYSCORE',
    key, 0, now - window)
local count = redis.call('ZCARD', key)
if count >= limit then
    return 0
end
redis.call('ZADD', key, now, now)
redis.call('EXPIRE', key, window)
return 1
"""

async def check_rate_limit(
    user_id: str,
    max_requests: int = 100,
    window_seconds: int = 60
) -> bool:
    """Check and record a request."""
    now = time.time()
    result = await _redis.eval(        #C
        RATE_LIMIT_SCRIPT,
        1,
        f"rate:{user_id}",
        max_requests,
        window_seconds,
        now
    )
    return bool(result)

async def rate_limit_middleware(
    request: Request,
    call_next
):
    """FastAPI middleware for limiting."""
    user = request.state.user_id
    if not await check_rate_limit(user):
        raise HTTPException(
            status_code=429,
            detail="Rate limit exceeded"
        )
    return await call_next(request)    #D
