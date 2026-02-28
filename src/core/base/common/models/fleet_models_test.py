# Auto-synced test for core/base/common/models/fleet_models.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "fleet_models.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "HealthCheckResult"), "HealthCheckResult missing"
    assert hasattr(mod, "IncrementalState"), "IncrementalState missing"
    assert hasattr(mod, "RateLimitConfig"), "RateLimitConfig missing"
    assert hasattr(mod, "TokenBudget"), "TokenBudget missing"
    assert hasattr(mod, "ShutdownState"), "ShutdownState missing"

