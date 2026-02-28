# Auto-synced test for infrastructure/engine/loading/kv_offload/models.py
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
    assert hasattr(mod, "OffloadMedium"), "OffloadMedium missing"
    assert hasattr(mod, "LoadStoreSpec"), "LoadStoreSpec missing"
    assert hasattr(mod, "BlockStatus"), "BlockStatus missing"
    assert hasattr(mod, "OffloadingEvent"), "OffloadingEvent missing"
    assert hasattr(mod, "PrepareStoreOutput"), "PrepareStoreOutput missing"

