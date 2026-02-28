# Auto-synced test for infrastructure/engine/pooling/pooling_metadata.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "pooling_metadata.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "PoolingStrategy"), "PoolingStrategy missing"
    assert hasattr(mod, "PoolingCursor"), "PoolingCursor missing"
    assert hasattr(mod, "PoolingStates"), "PoolingStates missing"
    assert hasattr(mod, "PoolingMetadata"), "PoolingMetadata missing"
    assert hasattr(mod, "Pooler"), "Pooler missing"
    assert hasattr(mod, "MeanPooler"), "MeanPooler missing"
    assert hasattr(mod, "MaxPooler"), "MaxPooler missing"
    assert hasattr(mod, "LastTokenPooler"), "LastTokenPooler missing"
    assert hasattr(mod, "AttentionWeightedPooler"), "AttentionWeightedPooler missing"
    assert hasattr(mod, "PoolerFactory"), "PoolerFactory missing"
    assert hasattr(mod, "PoolerOutput"), "PoolerOutput missing"
    assert hasattr(mod, "ChunkedPoolingManager"), "ChunkedPoolingManager missing"
    assert hasattr(mod, "pool_with_rust"), "pool_with_rust missing"

