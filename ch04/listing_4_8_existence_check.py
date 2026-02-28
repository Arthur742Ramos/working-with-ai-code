"""Listing 4.8 Quick existence check for recommended packages."""
import subprocess

def check_package_exists(
    name: str
) -> bool:
    """Check if a PyPI package exists."""
    result = subprocess.run(
        ["pip", "index", "versions", name],
        capture_output=True,
        text=True
    )
    return result.returncode == 0         # Returns False if the package is not found on PyPI
