"""Listing 4.6 A quick smoke test function for AI-generated code."""
import os
import subprocess
import tempfile
import sys

def smoke_test(code: str) -> dict:
    """Run AI-generated code in isolation."""
    with tempfile.NamedTemporaryFile(
        mode="w",
        suffix=".py",
        delete=False
    ) as f:
        f.write(code)
        f.flush()
    try:
        result = subprocess.run(
            [sys.executable, f.name],
            capture_output=True,
            text=True,
            timeout=10
        )
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "stdout": "",
            "stderr": "Timed out after 10 seconds"
        }
    finally:
        os.unlink(f.name)

    return {
        "success": result.returncode == 0,
        "stdout": result.stdout,
        "stderr": result.stderr
    }
