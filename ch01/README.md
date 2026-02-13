# Chapter 1: Working with AI -- from magic to tool

This chapter introduces the 3C Loop (Contract, Conversation, Checks) and does not include runnable code listings. Instead, it provides prompt examples that illustrate the difference between vague prompts and contract-style prompts.

## Key Prompts

### Vague prompt (what not to do)

```
Write me some code for handling errors.
```

### Contract-style prompt (what to do instead)

```
Write a Python function that wraps API calls with retry logic.

Requirements:
- Retry up to 3 times on transient errors (timeouts, 5xx responses)
- Use exponential backoff starting at 1 second
- Raise the original exception after retries fail
- Log each retry attempt with the error details
```

### Weak contract

```
Write a database migration to add user preferences.
```

### Strong contract

```
Write an Alembic migration to add a preferences JSONB column to the users table.
PostgreSQL 14. Default to empty object. Add an index for preferences->>'theme'.
Include both upgrade and downgrade functions.
```

## Concepts Introduced

- The myth of magic prompts
- Prompts as contracts (role, task, constraints, context)
- The 3C Loop: Contract, Conversation, Checks
- Judgment as the scarce skill
