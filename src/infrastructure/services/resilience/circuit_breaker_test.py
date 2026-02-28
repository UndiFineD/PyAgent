# Auto-synced test for infrastructure/services/resilience/circuit_breaker.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "circuit_breaker.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "CircuitState"), "CircuitState missing"
    assert hasattr(mod, "CircuitStats"), "CircuitStats missing"
    assert hasattr(mod, "CircuitBreakerError"), "CircuitBreakerError missing"
    assert hasattr(mod, "CircuitBreaker"), "CircuitBreaker missing"
    assert hasattr(mod, "CircuitBreakerRegistry"), "CircuitBreakerRegistry missing"
    assert hasattr(mod, "circuit_breaker"), "circuit_breaker missing"
    assert hasattr(mod, "get_circuit_stats"), "get_circuit_stats missing"
    assert hasattr(mod, "get_all_circuit_stats"), "get_all_circuit_stats missing"

