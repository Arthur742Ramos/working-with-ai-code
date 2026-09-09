-- Legacy source schema for the migration case.
-- Dates and account types use presentation-friendly strings.

CREATE TABLE legacy_users (
    id      INTEGER PRIMARY KEY,
    name    TEXT,
    email   TEXT,
    created TEXT,   -- "03/15/2024"
    type    TEXT    -- "1" or "2"
);
