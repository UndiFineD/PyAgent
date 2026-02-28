# Auto-synced test for infrastructure/engine/multimodal/encoder_cache_manager.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "encoder_cache_manager.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "CacheTier"), "CacheTier missing"
    assert hasattr(mod, "EvictionPolicy"), "EvictionPolicy missing"
    assert hasattr(mod, "CacheConfig"), "CacheConfig missing"
    assert hasattr(mod, "CacheEntry"), "CacheEntry missing"
    assert hasattr(mod, "CacheStats"), "CacheStats missing"
    assert hasattr(mod, "EncoderCacheManager"), "EncoderCacheManager missing"
    assert hasattr(mod, "MultiTierEncoderCache"), "MultiTierEncoderCache missing"
    assert hasattr(mod, "create_encoder_cache"), "create_encoder_cache missing"

