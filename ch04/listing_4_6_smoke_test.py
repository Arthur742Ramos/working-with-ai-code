import os
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
    try:
        mypy = subprocess.run(            #A
            [
                "mypy",
                "--ignore-missing-imports",
                path
            ],
            capture_output=True,
            text=True
        )

        ruff = subprocess.run(            #B
            ["ruff", "check", path],
            capture_output=True,
            text=True
        )
    finally:
        os.unlink(path)                   #C

    return {
        "mypy_ok": mypy.returncode == 0,
        "mypy_output": mypy.stdout,
        "ruff_ok": ruff.returncode == 0,
        "ruff_output": ruff.stdout
    }
