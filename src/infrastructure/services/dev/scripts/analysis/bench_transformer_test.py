# Auto-synced test for infrastructure/services/dev/scripts/analysis/bench_transformer.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "bench_transformer.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "run_performance_test"), "run_performance_test missing"

