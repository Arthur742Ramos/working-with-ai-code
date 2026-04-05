<!-- Listing 5.4: Transform pattern — SQL to ORM

From "Working with AI as a Real Teammate" (Manning)
Chapter 5
-->

Convert this SQL query to SQLAlchemy ORM (Python 3.11).
Preserve the exact logic including the LEFT JOIN
and the COALESCE default.

SELECT u.name, COALESCE(o.total, 0) as order_total
FROM users u
LEFT JOIN (
    SELECT user_id, SUM(amount) as total
    FROM orders
    WHERE created_at > '2024-01-01'
    GROUP BY user_id
) o ON u.id = o.user_id
WHERE u.active = true
ORDER BY order_total DESC;
