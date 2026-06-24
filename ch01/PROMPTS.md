# CH01 Prompts

Prompt blocks extracted from the current manuscript source.

These are the conversation prompts from the worked 3C Loop examples: refining an
Alembic migration, then adding rate limiting to a Flask endpoint across three turns.

## Alembic migration contract

````text
Write an Alembic migration to add a preferences JSONB column to the users table. PostgreSQL 14. Default to empty object. Add an index for preferences->>'theme'. Include both upgrade and downgrade functions.
````

## Adding a check constraint

````text
This looks good, but I also need a check constraint. It should ensure the JSON is always an object, not an array or primitive.
````

## Rate limiting request

````text
Here is a Flask endpoint in my app:

```python
@app.route("/api/upload", methods=["POST"])
@login_required
def upload():
    f = request.files["file"]
    save_upload(current_user.id, f)
    return {"ok": True}
```

Add rate limiting: at most 10 requests per minute per user. Keep it simple.
````

## Sharing state across instances

````text
This needs to work across multiple server instances behind a load balancer. The in-process counter won't be shared. We use redis-py; switch to Redis for shared state.
````

## Redis failure policy

````text
What happens if Redis is unavailable? Should requests fail open (allow) or fail closed (reject)?
````
