# Auto-synced test for infrastructure/services/dev/scripts/refactoring/move_imports_util.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "move_imports_util.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "fix_file"), "fix_file missing"
    assert hasattr(mod, "walk_dir"), "walk_dir missing"

