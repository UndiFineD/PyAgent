# Auto-synced test for core/base/logic/structures/ring_buffer.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "ring_buffer.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "RingBuffer"), "RingBuffer missing"
    assert hasattr(mod, "ThreadSafeRingBuffer"), "ThreadSafeRingBuffer missing"
    assert hasattr(mod, "TimestampedValue"), "TimestampedValue missing"
    assert hasattr(mod, "TimeSeriesBuffer"), "TimeSeriesBuffer missing"
    assert hasattr(mod, "SlidingWindowAggregator"), "SlidingWindowAggregator missing"

