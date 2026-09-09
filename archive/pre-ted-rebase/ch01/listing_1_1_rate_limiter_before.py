"""Listing 1.1: The rate limiter before the observability repair

From "Working with AI as a Real Teammate" (Manning)
Chapter 1
"""

def user_key():
    return str(current_user.id)


def on_limiter_fallback():
    app.logger.warning(
        "rate limiter entered in-memory fallback"
    )


limiter = Limiter(
    key_func=user_key,
    app=app,
    storage_uri=os.environ.get(
        "REDIS_URL",
        "memory://",
    ),
    in_memory_fallback_enabled=True,
)


@app.route("/api/upload", methods=["POST"])
@login_required
@limiter.limit("10 per minute")
def upload():
    f = request.files["file"]
    save_upload(current_user.id, f)
    return {"ok": True}
