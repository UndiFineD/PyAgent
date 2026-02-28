# Auto-synced test for interface/slash_commands/loader.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "loader.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "get_commands_dir"), "get_commands_dir missing"
    assert hasattr(mod, "discover_command_modules"), "discover_command_modules missing"
    assert hasattr(mod, "load_module"), "load_module missing"
    assert hasattr(mod, "unload_module"), "unload_module missing"
    assert hasattr(mod, "load_commands"), "load_commands missing"
    assert hasattr(mod, "reload_commands"), "reload_commands missing"
    assert hasattr(mod, "is_loaded"), "is_loaded missing"
    assert hasattr(mod, "get_loaded_modules"), "get_loaded_modules missing"

