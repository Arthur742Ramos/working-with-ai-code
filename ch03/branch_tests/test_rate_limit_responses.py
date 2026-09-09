"""Exercise the actual middleware stack without a Redis server."""
import asyncio
from pathlib import Path
import sys

import httpx
from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import rate_limit_redis as limiter


def make_app(monkeypatch, allowed):
    seen = []

    async def check(user_id):
        seen.append(("check", user_id))
        return allowed

    monkeypatch.setattr(limiter, "check_rate_limit", check)
    app = FastAPI()
    app.add_middleware(
        BaseHTTPMiddleware,
        dispatch=limiter.rate_limit_middleware,
    )

    @app.middleware("http")
    async def identity(request, call_next):
        request.state.user_id = "u1"
        return await call_next(request)

    @app.get("/resource")
    def resource():
        seen.append(("endpoint", "u1"))
        return {"ok": True}

    return app, seen


def request(app):
    async def run():
        transport = httpx.ASGITransport(
            app=app, raise_app_exceptions=False,
        )
        async with httpx.AsyncClient(
            transport=transport, base_url="http://test",
        ) as client:
            return await client.get("/resource")

    return asyncio.run(run())


def test_denial_returns_429_without_entering_endpoint(monkeypatch):
    app, seen = make_app(monkeypatch, False)
    response = request(app)
    assert response.status_code == 429
    assert response.json() == {"detail": "Rate limit exceeded"}
    assert seen == [("check", "u1")]


def test_allowance_reaches_endpoint_with_authenticated_identity(monkeypatch):
    app, seen = make_app(monkeypatch, True)
    response = request(app)
    assert response.status_code == 200
    assert response.json() == {"ok": True}
    assert seen == [("check", "u1"), ("endpoint", "u1")]
