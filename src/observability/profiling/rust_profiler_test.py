# Auto-synced test for observability/profiling/rust_profiler.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "rust_profiler.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "FunctionStats"), "FunctionStats missing"
    assert hasattr(mod, "RustProfiler"), "RustProfiler missing"
    assert hasattr(mod, "profile_rust_call"), "profile_rust_call missing"
    assert hasattr(mod, "RustUsageScanner"), "RustUsageScanner missing"
    assert hasattr(mod, "create_profiled_rust_core"), "create_profiled_rust_core missing"

