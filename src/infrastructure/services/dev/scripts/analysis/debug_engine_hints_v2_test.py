# Auto-synced test for infrastructure/services/dev/scripts/analysis/debug_engine_hints_v2.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "debug_engine_hints_v2.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "check_file_for_missing_hints"), "check_file_for_missing_hints missing"
    assert hasattr(mod, "scan_directory"), "scan_directory missing"

