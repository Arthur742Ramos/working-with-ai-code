"""Listing 4.4: A flawed money-handling function for two models to review

From "Working with AI as a Real Teammate" (Manning)
Chapter 4
"""


def charge(db, user_id, amount_cents):
    row = db.execute(
        "SELECT balance_cents FROM accounts "
        "WHERE user_id = %s" % user_id
    ).fetchone()
    bal = row["balance_cents"]
    if bal >= amount_cents:
        db.execute(
            "UPDATE accounts "
            "SET balance_cents = %d "
            "WHERE user_id = %d"
            % (bal - amount_cents, user_id)
        )
        return True
    return False
