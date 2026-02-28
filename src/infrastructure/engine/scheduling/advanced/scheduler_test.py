# Auto-synced test for infrastructure/engine/scheduling/advanced/scheduler.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "scheduler.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "AdvancedRequestScheduler"), "AdvancedRequestScheduler missing"
    assert hasattr(mod, "create_scheduler"), "create_scheduler missing"
    assert hasattr(mod, "priority_from_string"), "priority_from_string missing"

