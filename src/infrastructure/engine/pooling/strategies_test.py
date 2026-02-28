# Auto-synced test for infrastructure/engine/pooling/strategies.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "strategies.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "BasePooler"), "BasePooler missing"
    assert hasattr(mod, "MeanPooler"), "MeanPooler missing"
    assert hasattr(mod, "CLSPooler"), "CLSPooler missing"
    assert hasattr(mod, "LastTokenPooler"), "LastTokenPooler missing"
    assert hasattr(mod, "MaxPooler"), "MaxPooler missing"
    assert hasattr(mod, "AttentionPooler"), "AttentionPooler missing"
    assert hasattr(mod, "WeightedMeanPooler"), "WeightedMeanPooler missing"
    assert hasattr(mod, "MatryoshkaPooler"), "MatryoshkaPooler missing"
    assert hasattr(mod, "MultiVectorPooler"), "MultiVectorPooler missing"
    assert hasattr(mod, "StepPooler"), "StepPooler missing"

