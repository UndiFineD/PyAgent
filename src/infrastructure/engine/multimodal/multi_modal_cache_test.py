# Auto-synced test for infrastructure/engine/multimodal/multi_modal_cache.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "multi_modal_cache.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "MediaType"), "MediaType missing"
    assert hasattr(mod, "CacheBackend"), "CacheBackend missing"
    assert hasattr(mod, "HashAlgorithm"), "HashAlgorithm missing"
    assert hasattr(mod, "MediaHash"), "MediaHash missing"
    assert hasattr(mod, "CacheEntry"), "CacheEntry missing"
    assert hasattr(mod, "CacheStats"), "CacheStats missing"
    assert hasattr(mod, "PlaceholderRange"), "PlaceholderRange missing"
    assert hasattr(mod, "MultiModalHasher"), "MultiModalHasher missing"
    assert hasattr(mod, "MultiModalCache"), "MultiModalCache missing"
    assert hasattr(mod, "MemoryMultiModalCache"), "MemoryMultiModalCache missing"
    assert hasattr(mod, "PerceptualCache"), "PerceptualCache missing"
    assert hasattr(mod, "PrefetchMultiModalCache"), "PrefetchMultiModalCache missing"
    assert hasattr(mod, "IPCMultiModalCache"), "IPCMultiModalCache missing"
    assert hasattr(mod, "compute_media_hash"), "compute_media_hash missing"
    assert hasattr(mod, "create_cache"), "create_cache missing"

