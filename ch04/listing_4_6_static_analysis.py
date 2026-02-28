"""Listing 4.6 Running mypy and ruff on AI-generated code."""
import subprocess
import tempfile

def static_analysis(
    code: str
) -> dict:
    """Run type checking and linting."""
    with tempfile.NamedTemporaryFile(
        mode="w",
        suffix=".py",
        delete=False
    ) as f:
        f.write(code)
        path = f.name

    mypy = subprocess.run(                # Type checking catches type mismatches
        ["mypy", "--ignore-missing-imports",
         path],
        capture_output=True, text=True
    )

    ruff = subprocess.run(                # Linting catches style and logic issues
        ["ruff", "check", path],
        capture_output=True, text=True
    )

    return {
        "mypy_ok": mypy.returncode == 0,
        "mypy_output": mypy.stdout,
        "ruff_ok": ruff.returncode == 0,
        "ruff_output": ruff.stdout
    }
