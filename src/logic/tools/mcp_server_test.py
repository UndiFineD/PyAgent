# Auto-synced test for logic/tools/mcp_server.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "mcp_server.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "init_openspec"), "init_openspec missing"
    assert hasattr(mod, "create_sdd_spec"), "create_sdd_spec missing"
    assert hasattr(mod, "confirm_proceed"), "confirm_proceed missing"
    assert hasattr(mod, "create_task"), "create_task missing"
    assert hasattr(mod, "store_memory"), "store_memory missing"

