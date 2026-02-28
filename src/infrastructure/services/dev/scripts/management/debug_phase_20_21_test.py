# Auto-synced test for infrastructure/services/dev/scripts/management/debug_phase_20_21.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "debug_phase_20_21.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "test_visualization_and_memory"), "test_visualization_and_memory missing"
    assert hasattr(mod, "test_observability"), "test_observability missing"
    assert hasattr(mod, "test_gui_backend"), "test_gui_backend missing"

