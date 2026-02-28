# Auto-synced test for infrastructure/engine/pooling/pooling_engine.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "pooling_engine.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "PoolingTask"), "PoolingTask missing"
    assert hasattr(mod, "PoolingStrategy"), "PoolingStrategy missing"
    assert hasattr(mod, "PoolingConfig"), "PoolingConfig missing"
    assert hasattr(mod, "PoolingResult"), "PoolingResult missing"
    assert hasattr(mod, "EmbeddingOutput"), "EmbeddingOutput missing"
    assert hasattr(mod, "ClassificationOutput"), "ClassificationOutput missing"
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
    assert hasattr(mod, "PoolingEngine"), "PoolingEngine missing"
    assert hasattr(mod, "create_pooling_engine"), "create_pooling_engine missing"

