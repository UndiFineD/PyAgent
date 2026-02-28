# Auto-synced test for infrastructure/services/dev/scripts/management/repair_packages.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "repair_packages.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "create_inits"), "create_inits missing"
    assert hasattr(mod, "fix_imports"), "fix_imports missing"
    assert hasattr(mod, "main"), "main missing"

