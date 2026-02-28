# Auto-synced test for infrastructure/services/resilience/retry_strategy.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "retry_strategy.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "JitterType"), "JitterType missing"
    assert hasattr(mod, "RetryStats"), "RetryStats missing"
    assert hasattr(mod, "RetryExhaustedError"), "RetryExhaustedError missing"
    assert hasattr(mod, "RetryStrategy"), "RetryStrategy missing"
    assert hasattr(mod, "retry"), "retry missing"
    assert hasattr(mod, "RetryBudget"), "RetryBudget missing"

