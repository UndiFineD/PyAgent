# Auto-synced test for observability/stats/structured_counter.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "structured_counter.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "StructuredCounter"), "StructuredCounter missing"
    assert hasattr(mod, "CompilationCounter"), "CompilationCounter missing"
    assert hasattr(mod, "RequestCounter"), "RequestCounter missing"
    assert hasattr(mod, "CacheCounter"), "CacheCounter missing"
    assert hasattr(mod, "PoolCounter"), "PoolCounter missing"
    assert hasattr(mod, "QueueCounter"), "QueueCounter missing"
    assert hasattr(mod, "get_all_counters"), "get_all_counters missing"
    assert hasattr(mod, "reset_all_counters"), "reset_all_counters missing"

