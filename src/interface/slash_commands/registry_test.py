# Auto-synced test for interface/slash_commands/registry.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "registry.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "get_global_registry"), "get_global_registry missing"
    assert hasattr(mod, "reset_global_registry"), "reset_global_registry missing"
    assert hasattr(mod, "register"), "register missing"
    assert hasattr(mod, "register_command"), "register_command missing"
    assert hasattr(mod, "command"), "command missing"
    assert hasattr(mod, "unregister"), "unregister missing"
    assert hasattr(mod, "enable_command"), "enable_command missing"
    assert hasattr(mod, "disable_command"), "disable_command missing"
    assert hasattr(mod, "list_commands"), "list_commands missing"

