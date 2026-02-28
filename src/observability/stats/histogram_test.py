# Auto-synced test for observability/stats/histogram.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "histogram.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "HistogramBucket"), "HistogramBucket missing"
    assert hasattr(mod, "Histogram"), "Histogram missing"
    assert hasattr(mod, "ExponentialHistogram"), "ExponentialHistogram missing"
    assert hasattr(mod, "LatencyHistogram"), "LatencyHistogram missing"
    assert hasattr(mod, "SizeHistogram"), "SizeHistogram missing"

