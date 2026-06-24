"""Listing 4.16: A tiny eval: the cases that broke, scored on every run

From "Working with AI as a Real Teammate" (Manning)
Chapter 4

The full runnable script from code/ch04/tiny_eval.py. Freeze the
timestamp formats that broke in production, score a parser against
them, and rerun the check on every change. Run the Listing 4.1 regex
parser and it prints 2/5 passed; the spec-handling parser prints
5/5. The point is the move, not the parser: decide what "correct"
means on concrete inputs, then let a script keep score.

Run: python3 listing_4_16_tiny_eval.py
"""

import re
from datetime import datetime

# The cases that actually bit: a happy path,
# fractional seconds, a colon-free offset, a
# lowercase t separator, and a clear reject.
CASES = [
    ("2024-01-15T10:30:00Z",     True),
    ("2024-01-15T10:30:00.123Z", True),
    ("2024-01-15T10:30:00+0000", True),
    ("2024-01-15t10:30:00Z",     True),
    ("not-a-timestamp",          False),
]


def parse_regex(s):
    """The Listing 4.1 parser: happy path only."""
    pattern = (
        r"^\d{4}-\d{2}-\d{2}"
        r"T\d{2}:\d{2}:\d{2}"
        r"([+-]\d{2}:\d{2}|Z)$"
    )
    if not re.match(pattern, s):
        raise ValueError(f"Invalid: {s}")
    if s.endswith("Z"):
        s = s[:-1] + "+00:00"
    return datetime.fromisoformat(s)


def parse_fixed(s):
    """A parser that handles the spec variants."""
    s = s.replace("t", "T", 1)
    s = s.replace("Z", "+00:00")
    s = re.sub(r"([+-]\d{2})(\d{2})$", r"\1:\2", s)
    return datetime.fromisoformat(s)


def run_eval(parse):
    passed = 0
    for text, should_parse in CASES:
        try:
            parse(text)
            ok = should_parse
        except (ValueError, TypeError):
            ok = not should_parse
        passed += ok
        mark = "ok" if ok else "FAIL"
        print(f"{mark:4} {text}")
    print(f"{passed}/{len(CASES)} passed")
    return passed == len(CASES)


if __name__ == "__main__":
    print("regex parser (Listing 4.1):")
    run_eval(parse_regex)
    print("\nspec-handling parser (the fix):")
    run_eval(parse_fixed)
