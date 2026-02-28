# Auto-synced test for infrastructure/engine/sampling/kernels.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "kernels.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "TemperatureSampler"), "TemperatureSampler missing"
    assert hasattr(mod, "TopKSampler"), "TopKSampler missing"
    assert hasattr(mod, "TopPSampler"), "TopPSampler missing"
    assert hasattr(mod, "TopKTopPSampler"), "TopKTopPSampler missing"
    assert hasattr(mod, "GumbelSampler"), "GumbelSampler missing"
    assert hasattr(mod, "RepetitionPenaltySampler"), "RepetitionPenaltySampler missing"
    assert hasattr(mod, "PenaltySampler"), "PenaltySampler missing"

