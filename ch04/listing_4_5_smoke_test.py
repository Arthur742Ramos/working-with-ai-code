"""Listing 4.5 A quick smoke test function for AI-generated code."""
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

        result = subprocess.run(          # Running the code as a separate process
            [sys.executable, f.name],
            capture_output=True,
            text=True,
            timeout=10                    # Timeout prevents infinite loops
        )

    return {
        "success": result.returncode == 0,
        "stdout": result.stdout,
        "stderr": result.stderr
    }
