# Auto-synced test for core/base/common/utils/hash_registry.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "hash_registry.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "HashAlgorithm"), "HashAlgorithm missing"
    assert hasattr(mod, "is_fips_mode"), "is_fips_mode missing"
    assert hasattr(mod, "hash_sha256"), "hash_sha256 missing"
    assert hasattr(mod, "hash_sha1"), "hash_sha1 missing"
    assert hasattr(mod, "hash_md5"), "hash_md5 missing"
    assert hasattr(mod, "hash_xxhash64"), "hash_xxhash64 missing"
    assert hasattr(mod, "hash_xxhash128"), "hash_xxhash128 missing"
    assert hasattr(mod, "hash_fnv1a"), "hash_fnv1a missing"
    assert hasattr(mod, "safe_hash"), "safe_hash missing"
    assert hasattr(mod, "get_hash_fn"), "get_hash_fn missing"
    assert hasattr(mod, "get_hash_fn_by_name"), "get_hash_fn_by_name missing"
    assert hasattr(mod, "hash_with"), "hash_with missing"
    assert hasattr(mod, "ContentHasher"), "ContentHasher missing"
    assert hasattr(mod, "default_hasher"), "default_hasher missing"
    assert hasattr(mod, "fast_hasher"), "fast_hasher missing"
    assert hasattr(mod, "cache_hasher"), "cache_hasher missing"
    assert hasattr(mod, "XXHASH_AVAILABLE"), "XXHASH_AVAILABLE missing"
    assert hasattr(mod, "RUST_AVAILABLE"), "RUST_AVAILABLE missing"

