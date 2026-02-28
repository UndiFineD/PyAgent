# Auto-synced test for infrastructure/engine/kv_cache/managers.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "managers.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "SingleTypeKVCacheManager"), "SingleTypeKVCacheManager missing"
    assert hasattr(mod, "FullAttentionManager"), "FullAttentionManager missing"
    assert hasattr(mod, "SlidingWindowManager"), "SlidingWindowManager missing"
    assert hasattr(mod, "CrossAttentionManager"), "CrossAttentionManager missing"

