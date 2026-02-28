# Auto-synced test for infrastructure/services/api/agent_api_server.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "agent_api_server.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "TaskRequest"), "TaskRequest missing"
    assert hasattr(mod, "TelemetryManager"), "TelemetryManager missing"
    assert hasattr(mod, "root"), "root missing"
    assert hasattr(mod, "list_agents"), "list_agents missing"
    assert hasattr(mod, "list_discovery_peers"), "list_discovery_peers missing"
    assert hasattr(mod, "list_fastest_peers"), "list_fastest_peers missing"
    assert hasattr(mod, "dispatch_task"), "dispatch_task missing"
    assert hasattr(mod, "websocket_endpoint"), "websocket_endpoint missing"

