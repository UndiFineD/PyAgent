# Auto-synced test for infrastructure/services/dev/scripts/maintenance/version.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "version.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "is_gate_open"), "is_gate_open missing"
    assert hasattr(mod, "get_version_info"), "get_version_info missing"

