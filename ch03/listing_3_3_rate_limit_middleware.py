import time

import redis.asyncio as redis
from fastapi import HTTPException, Request

_redis = redis.from_url(              #A
    "redis://localhost:6379"
)

async def check_rate_limit(
    user_id: str,
    max_requests: int = 100,
    window_seconds: int = 60,
) -> bool:
    now = time.time()
    result = await _redis.eval(       #B
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
    user = request.state.user_id      #C
    allowed = await check_rate_limit(user)
    if not allowed:
        raise HTTPException(
            status_code=429,
            detail="Rate limit exceeded",
        )
    return await call_next(request)   #D
