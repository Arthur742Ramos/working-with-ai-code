# Chapter 5 — Code Listings

The four prompt building blocks (role, constraints, examples, steps) and
the four task categories (explain, transform, generate, critique), ending
in a data-migration case study where an explicit operational contract turns
an irreversible task into a reviewable one.

- **`listing_5_1_universal_task_template.md`** — Listing 5.1: The universal task template
- **`listing_5_2_test_cases.py`** — Listing 5.2: Using test cases to constrain a function
- **`listing_5_3_structured_json.md`** — Listing 5.3: Requesting structured JSON output
- **`listing_5_4_transform_sql_to_orm.md`** — Listing 5.4: Transform category: SQL to ORM
- **`listing_5_5_generate_api_endpoint.md`** — Listing 5.5: Generate category: API endpoint with full contract
- **`listing_5_6_legacy_schema.sql`** — Listing 5.6: Legacy source schema (`legacy_users`)
- **`listing_5_7_target_schema.sql`** — Listing 5.7: Target schema (`accounts` and audit)
- **`PROMPTS.md`** — Prompt blocks from the current manuscript draft

Most chapter 5 listings are prompt templates rather than runnable Python code.
Listing 5.2 defines the test cases that constrain a `slugify` specification.
Listings 5.6 and 5.7 are the legacy and target schemas for the migration case
study (`code/ch05/schema_legacy.sql` and `code/ch05/schema_new.sql` in the
book repo); the chapter's migration prompts name the target `schema_new.sql`.

See the [main README](../README.md) for setup instructions.
