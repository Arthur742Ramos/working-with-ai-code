import time
from functools import wraps
from collections import defaultdict
from fastapi import HTTPException, Request

# In-memory store: {user_id: [timestamps]}
_hits: dict[str, list[float]] = (
    defaultdict(list)
)

def rate_limit(
    max_requests: int = 100,
    window_seconds: int = 60
):
    """Rate-limit decorator for FastAPI."""
    def decorator(func):
        @wraps(func)
        async def wrapper(
            request: Request,
            *args, **kwargs
        ):
            user = request.state.user_id  #A
            now = time.monotonic()
            cutoff = now - window_seconds

            # Dropping expired timestamps
            _hits[user] = [
                t for t in _hits[user]
                if t > cutoff
            ]

            if len(_hits[user]) >= max_requests:
                raise HTTPException(   #B
                    status_code=429,
                    detail="Rate limit exceeded"
                )

            _hits[user].append(now)
            return await func(
                request, *args, **kwargs
            )
        return wrapper
    return decorator

@rate_limit(max_requests=100)          #C
async def get_users(request: Request):
    return {"users": []}
