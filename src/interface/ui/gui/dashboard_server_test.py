# Auto-synced test for interface/ui/gui/dashboard_server.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "dashboard_server.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "ConnectionManager"), "ConnectionManager missing"
    assert hasattr(mod, "get_version"), "get_version missing"
    assert hasattr(mod, "get_health"), "get_health missing"
    assert hasattr(mod, "get_status"), "get_status missing"
    assert hasattr(mod, "get_logs"), "get_logs missing"
    assert hasattr(mod, "get_thoughts"), "get_thoughts missing"
    assert hasattr(mod, "list_artifacts"), "list_artifacts missing"
    assert hasattr(mod, "websocket_telemetry"), "websocket_telemetry missing"

