# Auto-synced test for core/base/common/utils/atomic_counter.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "atomic_counter.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "Counter"), "Counter missing"
    assert hasattr(mod, "AtomicCounter"), "AtomicCounter missing"
    assert hasattr(mod, "AtomicFlag"), "AtomicFlag missing"
    assert hasattr(mod, "AtomicGauge"), "AtomicGauge missing"
    assert hasattr(mod, "RUST_AVAILABLE"), "RUST_AVAILABLE missing"

