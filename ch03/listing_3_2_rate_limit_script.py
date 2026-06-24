"""Listing 3.2: Branch B result, part 1: Redis sliding-window script

From "Working with AI as a Real Teammate" (Manning)
Chapter 3
"""

RATE_LIMIT_SCRIPT = """
local key = KEYS[1]
local limit = tonumber(ARGV[1])
local window = tonumber(ARGV[2])
local now = tonumber(ARGV[3])

redis.call(
    "ZREMRANGEBYSCORE",
    key,
    0,
    now - window
)
local count = redis.call("ZCARD", key)
if count >= limit then
    return 0
end
redis.call("ZADD", key, now, now)
redis.call("EXPIRE", key, window)
return 1
"""
