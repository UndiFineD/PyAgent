# Auto-synced test for infrastructure/engine/engine_core_client.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "engine_core_client.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "RequestType"), "RequestType missing"
    assert hasattr(mod, "ClientConfig"), "ClientConfig missing"
    assert hasattr(mod, "EngineCoreClient"), "EngineCoreClient missing"
    assert hasattr(mod, "InprocClient"), "InprocClient missing"
    assert hasattr(mod, "SyncMPClient"), "SyncMPClient missing"
    assert hasattr(mod, "AsyncMPClient"), "AsyncMPClient missing"
    assert hasattr(mod, "create_client"), "create_client missing"

