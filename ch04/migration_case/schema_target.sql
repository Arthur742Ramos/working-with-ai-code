-- Target schema for normalized accounts and migration audit data.

CREATE TABLE accounts (
    id           INTEGER PRIMARY KEY,
    full_name    TEXT,
    email        TEXT,
    created_at   TIMESTAMP,
    account_type TEXT   -- "individual" or "business"
);

CREATE TABLE account_migration_audit (
    account_id INTEGER,
    field_name TEXT,
    old_value  TEXT,
    new_value  TEXT
);
