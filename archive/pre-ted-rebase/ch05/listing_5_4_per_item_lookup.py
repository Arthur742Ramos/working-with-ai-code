"""Listing 5.4: The per-item lookup in the shipped summary path

From "Working with AI as a Real Teammate" (Manning)
Chapter 5

Excerpt from the shipped summary path: `items`, `con`, `lookup_product`,
`total`, and `lines` come from the surrounding function.
"""

for item in items:
    product = lookup_product(con, item["code"])
    price = product["price"]
    line_total = price * item["qty"]
    total += line_total
    lines.append({
        "code": item["code"],
        "name": product["name"],
        "qty": item["qty"],
        "line_total": round(line_total, 2),
    })
