import sqlite3

connection = sqlite3.connect(":memory:")
connection.row_factory = sqlite3.Row
row = connection.execute(
    "SELECT NULL AS snoozed_until"
).fetchone()
assert row["snoozed_until"] is None
try:
    row.get("snoozed_until")
except AttributeError as error:
    print(type(error).__name__ + ": " + str(error))
finally:
    connection.close()
