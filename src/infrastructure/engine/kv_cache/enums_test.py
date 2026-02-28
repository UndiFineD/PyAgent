# Auto-synced test for infrastructure/engine/kv_cache/enums.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "enums.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "CacheGroupType"), "CacheGroupType missing"
    assert hasattr(mod, "AllocationStrategy"), "AllocationStrategy missing"
    assert hasattr(mod, "EvictionPolicy"), "EvictionPolicy missing"

