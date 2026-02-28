# Auto-synced test for infrastructure/engine/prefix_cache_manager.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "prefix_cache_manager.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "HashAlgorithm"), "HashAlgorithm missing"
    assert hasattr(mod, "BlockHash"), "BlockHash missing"
    assert hasattr(mod, "CacheBlock"), "CacheBlock missing"
    assert hasattr(mod, "get_hash_function"), "get_hash_function missing"
    assert hasattr(mod, "hash_block_tokens"), "hash_block_tokens missing"
    assert hasattr(mod, "hash_block_tokens_rust"), "hash_block_tokens_rust missing"
    assert hasattr(mod, "init_none_hash"), "init_none_hash missing"
    assert hasattr(mod, "PrefixCacheManager"), "PrefixCacheManager missing"
    assert hasattr(mod, "compute_prefix_match"), "compute_prefix_match missing"
    assert hasattr(mod, "compute_prefix_match_rust"), "compute_prefix_match_rust missing"
    assert hasattr(mod, "compute_cache_keys"), "compute_cache_keys missing"
    assert hasattr(mod, "compute_cache_keys_rust"), "compute_cache_keys_rust missing"

