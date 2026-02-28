# Auto-synced test for infrastructure/engine/loading/kv_offload_manager.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "kv_offload_manager.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "ARCOffloadingManager"), "ARCOffloadingManager missing"
    assert hasattr(mod, "BlockHash"), "BlockHash missing"
    assert hasattr(mod, "BlockStatus"), "BlockStatus missing"
    assert hasattr(mod, "LoadStoreSpec"), "LoadStoreSpec missing"
    assert hasattr(mod, "LRUOffloadingManager"), "LRUOffloadingManager missing"
    assert hasattr(mod, "MemoryBackend"), "MemoryBackend missing"
    assert hasattr(mod, "OffloadMedium"), "OffloadMedium missing"
    assert hasattr(mod, "OffloadingBackend"), "OffloadingBackend missing"
    assert hasattr(mod, "OffloadingEvent"), "OffloadingEvent missing"
    assert hasattr(mod, "OffloadingManager"), "OffloadingManager missing"
    assert hasattr(mod, "PrepareStoreOutput"), "PrepareStoreOutput missing"
    assert hasattr(mod, "TieredOffloadManager"), "TieredOffloadManager missing"

