# Auto-synced test for infrastructure/engine/pooling/models.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "models.py"
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

