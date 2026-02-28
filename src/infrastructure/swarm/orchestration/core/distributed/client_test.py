# Auto-synced test for infrastructure/swarm/orchestration/core/distributed/client.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "client.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "MPClient"), "MPClient missing"
    assert hasattr(mod, "AsyncMPClient"), "AsyncMPClient missing"
    assert hasattr(mod, "DPLBAsyncMPClient"), "DPLBAsyncMPClient missing"

