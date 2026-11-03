"""Platform-independent ordering checks for the capture's current inventory."""
import importlib.util
from pathlib import Path, PurePosixPath, PureWindowsPath
import unittest
from unittest.mock import patch


PACKAGE_ROOT = Path(__file__).resolve().parents[1]
CAPTURE_ROOT = PACKAGE_ROOT / "captures" / "incident_orphan_product_policy"
SPEC = importlib.util.spec_from_file_location(
    "incident_capture_runner", CAPTURE_ROOT / "run_capture.py"
)
RUNNER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(RUNNER)


class CandidatePath:
    """Supply file methods while retaining the selected PurePath ordering."""

    def __init__(self, value):
        self.value = value

    def __lt__(self, other):
        return self.value < other.value

    @property
    def name(self):
        return self.value.name

    @property
    def suffix(self):
        return self.value.suffix

    def is_file(self):
        return True

    def relative_to(self, root):
        return self.value.relative_to(root.value)


class InventoryRoot:
    def __init__(self, value, names):
        self.value = value
        self.files = [CandidatePath(value / name) for name in names]

    def rglob(self, pattern):
        return iter(self.files)


class CaptureInventoryTests(unittest.TestCase):
    def check_order(self, path_type, root_name):
        names = [
            "seed.py",
            "captures/incident_orphan_product_policy/patches/missing-product-policy.diff",
            "captures/incident_orphan_product_policy/before/seed.py",
            "README.md",
            "captures/incident_orphan_product_policy/README.md",
            "captures/incident_orphan_product_policy/patches/README.md",
            "server.log",
            "__pycache__/server.pyc",
        ]
        expected = [
            "README.md",
            "captures/incident_orphan_product_policy/README.md",
            "captures/incident_orphan_product_policy/before/seed.py",
            "captures/incident_orphan_product_policy/patches/README.md",
            "captures/incident_orphan_product_policy/patches/missing-product-policy.diff",
            "seed.py",
        ]
        root = InventoryRoot(path_type(root_name), names)
        with patch.object(RUNNER, "PACKAGE_ROOT", root):
            observed = [
                path.relative_to(root).as_posix()
                for path in RUNNER.maintained_package_files()
            ]
            self.assertEqual(observed, expected)
            RUNNER.verify_package_inventory({"package_inventory": expected})

    def test_windows_paths_use_case_sensitive_posix_inventory_order(self):
        self.check_order(PureWindowsPath, "C:/fixture/ch05")

    def test_posix_paths_use_the_same_inventory_order(self):
        self.check_order(PurePosixPath, "/fixture/ch05")

    def test_live_package_matches_recorded_inventory(self):
        # The frozen capture's inventory describes its historical package.
        # The follow-on manifest binds the current, expanded publication instead.
        spec = importlib.util.spec_from_file_location(
            "publication_checks", PACKAGE_ROOT / "run_checks.py"
        )
        publication = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(publication)
        publication.verify_publication()


if __name__ == "__main__":
    unittest.main()
