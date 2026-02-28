# Auto-synced test for infrastructure/storage/kv_transfer/arc_offload_manager.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "arc_offload_manager.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "BlockHash"), "BlockHash missing"
    assert hasattr(mod, "OffloadMedium"), "OffloadMedium missing"
    assert hasattr(mod, "BlockState"), "BlockState missing"
    assert hasattr(mod, "BlockStatus"), "BlockStatus missing"
    assert hasattr(mod, "LoadStoreSpec"), "LoadStoreSpec missing"
    assert hasattr(mod, "OffloadingEvent"), "OffloadingEvent missing"
    assert hasattr(mod, "PrepareStoreOutput"), "PrepareStoreOutput missing"
    assert hasattr(mod, "Backend"), "Backend missing"
    assert hasattr(mod, "SimpleBackend"), "SimpleBackend missing"
    assert hasattr(mod, "OffloadingManager"), "OffloadingManager missing"
    assert hasattr(mod, "ARCOffloadManager"), "ARCOffloadManager missing"
    assert hasattr(mod, "AdaptiveARCManager"), "AdaptiveARCManager missing"
    assert hasattr(mod, "AsyncARCManager"), "AsyncARCManager missing"

