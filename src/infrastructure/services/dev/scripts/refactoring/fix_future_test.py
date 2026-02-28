# Auto-synced test for infrastructure/services/dev/scripts/refactoring/fix_future.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "fix_future.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert mod is not None

