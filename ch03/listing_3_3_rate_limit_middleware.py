"""Listing 3.3: Branch B result, part 2: Python wrapper and middleware.

From "Working with AI as a Real Teammate" (Manning)
Chapter 3
"""

import time

import redis.asyncio as redis
from fastapi import HTTPException, Request

from listing_3_2_rate_limit_script import RATE_LIMIT_SCRIPT

_redis = redis.from_url(
    "redis://localhost:6379"
)


async def check_rate_limit(
    user_id: str,
    max_requests: int = 100,
    window_seconds: int = 60,
) -> bool:
    now = time.time()
    result = await _redis.eval(
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
    user = request.state.user_id
    allowed = await check_rate_limit(user)
    if not allowed:
        raise HTTPException(
            status_code=429,
            detail="Rate limit exceeded",
        )
    return await call_next(request)
