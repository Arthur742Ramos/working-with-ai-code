"""Executable guard: feature modules may use only the house HTTP client."""

import ast
import os
from dataclasses import dataclass
from pathlib import Path

HERE = Path(__file__).parent
SOURCE_ROOT = Path(os.environ.get("HOUSE_RULE_ROOT", HERE))

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
        relative_path = self.path.relative_to(root)
        return (
            f"{relative_path}:{self.line}: "
            f"unapproved outbound HTTP import: {self.module}"
        )


def feature_modules(root: Path):
    for path in sorted(root.glob("*.py")):
        if path.name.startswith("test_") or path.name in ALLOWED_MODULES:
            continue
        yield path


def imported_modules(tree: ast.AST):
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                yield node.lineno, alias.name
        elif isinstance(node, ast.ImportFrom) and node.module:
            yield node.lineno, node.module


def find_unapproved_http_imports(root: Path):
    violations = []
    for path in feature_modules(root):
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for line, module in imported_modules(tree):
            root_module = module.split(".", 1)[0]
            if root_module in UNAPPROVED_HTTP_MODULES:
                violations.append(Violation(path, line, module))
    return violations


def test_no_unapproved_http_clients():
    violations = find_unapproved_http_imports(SOURCE_ROOT)
    details = "\n".join(
        violation.display(SOURCE_ROOT) for violation in violations
    )
    assert not violations, (
        "outbound HTTP must go through http_client.call; "
        f"found direct transport imports:\n{details}"
    )


def test_direct_requests_fixture_proves_guard_is_live():
    fixture_root = HERE / "fixtures" / "direct_requests"
    violations = find_unapproved_http_imports(fixture_root)

    assert [item.display(fixture_root) for item in violations] == [
        "alerts.py:3: unapproved outbound HTTP import: requests"
    ]
