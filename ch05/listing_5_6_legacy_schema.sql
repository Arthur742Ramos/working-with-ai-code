-- Listing 5.6: Legacy source schema (legacy_users)
--
-- From "Working with AI as a Real Teammate" (Manning)
-- Chapter 5

CREATE TABLE legacy_users (
    id      INTEGER PRIMARY KEY,
    name    TEXT,
    email   TEXT,
    created TEXT,   -- "03/15/2024"
    type    TEXT    -- "1" or "2"
);
