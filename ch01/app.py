"""Runnable fallback-observability fixture.

The module retains a per-user, ten-per-minute limit, uses
Redis when configured, and falls back to a bounded in-memory
counter when Redis is unavailable. The captured repair adds
one logger assignment without changing that policy.

Listing 1.1 prints the relevant before-state excerpt. This
complete module includes the surrounding Flask,
authentication, upload, and command-line scaffolding needed
to run the checks.
"""

import os

from flask import Flask, request

# --- Minimal auth glue -------------------------------------
# The chapter's snippets use @login_required and
# current_user from a flask-login-style setup. In a real app
# these come from Flask-Login. Here we provide the smallest
# stand-ins so the rate-limiting code shown in the chapter is
# the part you actually exercise.
try:
    from flask_login import (  # type: ignore
        LoginManager,
        current_user,
        login_required,
    )

    _HAVE_FLASK_LOGIN = True
except ImportError:  # pragma: no cover - fallback stubs
    _HAVE_FLASK_LOGIN = False

    class _AnonUser:
        id = "demo-user"

    current_user = _AnonUser()

    def login_required(f):
        return f


app = Flask(__name__)

if _HAVE_FLASK_LOGIN:
    login_manager = LoginManager()
    login_manager.init_app(app)


def save_upload(user_id, f):
    """Persist an uploaded file for a user.

    Stub for the chapter's example; a real implementation
    would stream the file to object storage or disk.
    """
    dest = os.path.join("/tmp", f"upload-{user_id}")
    f.save(dest)
    return dest


from flask_limiter import Limiter  # noqa: E402


def user_key():
    return str(current_user.id)


limiter = Limiter(
    key_func=user_key,
    app=app,
    storage_uri=os.environ.get("REDIS_URL", "memory://"),
    # Keep uploads bounded if shared storage is unavailable.
    in_memory_fallback_enabled=True,
)
limiter.logger = app.logger


@app.route("/api/upload", methods=["POST"])
@login_required
@limiter.limit("10 per minute")
def upload():
    f = request.files["file"]
    save_upload(current_user.id, f)
    return {"ok": True}


if __name__ == "__main__":
    # Set REDIS_URL to point at a real Redis for shared,
    # cross-instance limits, e.g.:
    #   export REDIS_URL=redis://localhost:6379
    # Without it, the limiter uses in-process memory storage.
    app.run(port=int(os.environ.get("PORT", "5000")))
