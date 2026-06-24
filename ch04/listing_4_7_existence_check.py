"""Listing 4.7: Quick existence check for recommended packages

From "Working with AI as a Real Teammate" (Manning)
Chapter 4
"""

import subprocess
import sys


def check_package_exists(
    name: str
) -> bool:
    """Check if a PyPI package exists."""
    result = subprocess.run(
        [sys.executable, "-m", "pip",
         "index", "versions", name],
        capture_output=True,
        text=True
    )
    return result.returncode == 0
