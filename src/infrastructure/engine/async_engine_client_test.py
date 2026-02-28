# Auto-synced test for infrastructure/engine/async_engine_client.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "async_engine_client.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "ClientMode"), "ClientMode missing"
    assert hasattr(mod, "WorkerState"), "WorkerState missing"
    assert hasattr(mod, "EngineClientConfig"), "EngineClientConfig missing"
    assert hasattr(mod, "SchedulerOutput"), "SchedulerOutput missing"
    assert hasattr(mod, "EngineOutput"), "EngineOutput missing"
    assert hasattr(mod, "WorkerInfo"), "WorkerInfo missing"
    assert hasattr(mod, "EngineCoreClientBase"), "EngineCoreClientBase missing"
    assert hasattr(mod, "InprocClient"), "InprocClient missing"
    assert hasattr(mod, "SyncMPClient"), "SyncMPClient missing"
    assert hasattr(mod, "AsyncMPClient"), "AsyncMPClient missing"
    assert hasattr(mod, "P2CLoadBalancer"), "P2CLoadBalancer missing"
    assert hasattr(mod, "DPAsyncMPClient"), "DPAsyncMPClient missing"
    assert hasattr(mod, "auto_select_client_mode"), "auto_select_client_mode missing"
    assert hasattr(mod, "create_engine_client"), "create_engine_client missing"

