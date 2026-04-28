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
    return result.returncode == 0         #A
