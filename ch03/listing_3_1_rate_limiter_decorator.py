import time
from collections import defaultdict
from functools import wraps

from fastapi import HTTPException, Request

_hits: dict[str, list[float]] = (
    defaultdict(list)
)

def rate_limit(
    max_requests: int = 100,
    window_seconds: int = 60,
):
    def decorator(func):
        @wraps(func)
        async def wrapper(
            request: Request,
            *args,
            **kwargs,
        ):
            user = request.state.user_id  #A
            now = time.monotonic()
            cutoff = now - window_seconds

            _hits[user] = [               #B
                t for t in _hits[user]
                if t > cutoff
            ]
            if len(_hits[user]) >= max_requests:
                raise HTTPException(      #C
                    status_code=429,
                    detail="Rate limit exceeded",
                )
            _hits[user].append(now)
            return await func(
                request,
                *args,
                **kwargs,
            )

        return wrapper

    return decorator
