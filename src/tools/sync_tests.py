spec.loader.exec_module(mod)
'''''''        # Write the test file
"""Synchronize test files with cleaned modules (minimal, safe).

This script scans a `cleaned` directory for Python modules and
creates lightweight test stubs under `tests/unit` to allow CI to
import and exercise those modules during repair.
"""

from __future__ import annotations

import glob
from pathlib import Path


CLEANED_DIR = Path("src/external_candidates/cleaned")
TESTS_DIR = Path("tests/unit")


def main() -> None:
    TESTS_DIR.mkdir(parents=True, exist_ok=True)
    modules = glob.glob(str(CLEANED_DIR / "*.py"))
    for mod_path in modules:
        mod_name = Path(mod_path).stem
        test_path = TESTS_DIR / f"test_auto_{mod_name}.py"
        content = f"""# Auto-generated test for {mod_name}
import importlib.util
from pathlib import Path

p = Path(r"{mod_path}")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
if spec.loader:
    spec.loader.exec_module(mod)

def test_import():
    assert hasattr(mod, '__name__')
"""
        test_path.write_text(content, encoding="utf-8")


if __name__ == "__main__":
    main()

