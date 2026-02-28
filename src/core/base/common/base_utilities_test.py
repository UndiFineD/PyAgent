# Auto-synced test for core/base/common/base_utilities.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "base_utilities.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "strip_ansi_codes"), "strip_ansi_codes missing"
    assert hasattr(mod, "bulk_replace"), "bulk_replace missing"
    assert hasattr(mod, "setup_logging"), "setup_logging missing"
    assert hasattr(mod, "as_tool"), "as_tool missing"
    assert hasattr(mod, "create_main_function"), "create_main_function missing"

