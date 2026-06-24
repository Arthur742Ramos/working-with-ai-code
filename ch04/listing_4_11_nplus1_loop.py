"""Listing 4.11: The N+1 loop at the heart of build_summary

From "Working with AI as a Real Teammate" (Manning)
Chapter 4

Excerpt from code/ch04/incident_demo/server.py (the original shipped,
buggy build_summary). Both bugs are visible at once: an unguarded None
from lookup_product, and one unindexed product query per line item.
"""

# Classic N+1: one product query per line
# item, each an unindexed full scan.
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
