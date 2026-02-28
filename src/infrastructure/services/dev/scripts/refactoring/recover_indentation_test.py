# Auto-synced test for infrastructure/services/dev/scripts/refactoring/recover_indentation.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "recover_indentation.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "fix_broken_indentation"), "fix_broken_indentation missing"

