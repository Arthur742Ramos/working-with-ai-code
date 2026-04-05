<!-- Listing 5.5: Generate pattern — API endpoint with full contract

From "Working with AI as a Real Teammate" (Manning)
Chapter 5
-->

Role: Backend developer working on a Flask REST API.

Generate a POST endpoint for /api/invoices that:
- Accepts JSON with fields: customer_id (int),
  items (list of {description: str, amount: float}),
  due_date (ISO 8601 string)
- Validates all fields, returns 400 with specific
  error messages for invalid input
- Stores the invoice and returns 201 with the
  created invoice including a generated invoice_id
- Uses SQLAlchemy for persistence

Constraints:
- No global state; use Flask's app context
- Return JSON error responses, not HTML
- Include type hints
