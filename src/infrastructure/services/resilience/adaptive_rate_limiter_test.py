# Auto-synced test for infrastructure/services/resilience/adaptive_rate_limiter.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "adaptive_rate_limiter.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "RateLimitExceededError"), "RateLimitExceededError missing"
    assert hasattr(mod, "RateLimiterStats"), "RateLimiterStats missing"
    assert hasattr(mod, "TokenBucket"), "TokenBucket missing"
    assert hasattr(mod, "SlidingWindowCounter"), "SlidingWindowCounter missing"
    assert hasattr(mod, "AdaptiveRateLimiter"), "AdaptiveRateLimiter missing"
    assert hasattr(mod, "PerKeyRateLimiter"), "PerKeyRateLimiter missing"
    assert hasattr(mod, "rate_limit"), "rate_limit missing"

