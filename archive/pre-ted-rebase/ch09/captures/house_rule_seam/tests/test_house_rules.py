"""Capture copy of the direct-transport import guard."""

import ast
from dataclasses import dataclass
from pathlib import Path


HERE = Path(__file__).parents[1]
ALLOWED_MODULES = {"http_client.py"}
UNAPPROVED_HTTP_MODULES = {
    "aiohttp",
    "http",
    "httpx",
    "requests",
    "socket",
    "urllib",
}


@dataclass(frozen=True)
class Violation:
    path: Path
    line: int
    module: str

    def display(self, root: Path) -> str:
        return (
            f"{self.path.relative_to(root)}:{self.line}: "
            f"unapproved outbound HTTP import: {self.module}"
        )


def feature_modules(root: Path):
    for path in sorted(root.glob("*.py")):
        if path.name.startswith("test_") or path.name in ALLOWED_MODULES:
            continue
        yield path


def find_unapproved_http_imports(root: Path):
    violations = []
    for path in feature_modules(root):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                modules = [alias.name for alias in node.names]
            elif isinstance(node, ast.ImportFrom) and node.module:
                modules = [node.module]
            else:
                continue
            for module in modules:
                if module.split(".", 1)[0] in UNAPPROVED_HTTP_MODULES:
                    violations.append(
                        Violation(path, node.lineno, module)
                    )
    return violations


def test_no_unapproved_http_clients():
    violations = find_unapproved_http_imports(HERE)
    details = "\n".join(item.display(HERE) for item in violations)
    assert not violations, (
        "outbound HTTP must go through http_client.call; "
        f"found direct transport imports:\n{details}"
    )


def test_direct_requests_source_proves_guard_is_live(tmp_path):
    source = tmp_path / "alerts.py"
    source.write_text("import requests\n", encoding="utf-8")

    violations = find_unapproved_http_imports(tmp_path)

    assert [(item.line, item.module) for item in violations] == [
        (1, "requests")
    ]
