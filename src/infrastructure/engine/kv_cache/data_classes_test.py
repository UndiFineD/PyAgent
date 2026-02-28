# Auto-synced test for infrastructure/engine/kv_cache/data_classes.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "data_classes.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "BlockHash"), "BlockHash missing"
    assert hasattr(mod, "BlockHashWithGroupId"), "BlockHashWithGroupId missing"
    assert hasattr(mod, "KVCacheBlock"), "KVCacheBlock missing"
    assert hasattr(mod, "KVCacheBlocks"), "KVCacheBlocks missing"
    assert hasattr(mod, "CacheGroupSpec"), "CacheGroupSpec missing"
    assert hasattr(mod, "CacheConfig"), "CacheConfig missing"

