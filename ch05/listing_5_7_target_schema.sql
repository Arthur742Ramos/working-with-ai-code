-- Listing 5.7: Target schema (accounts and audit)
--
-- From "Working with AI as a Real Teammate" (Manning)
-- Chapter 5
--
-- The chapter's migration prompts name this file schema_new.sql.

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
