# Auto-synced test for interface/slash_commands/commands/system.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "system.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "cmd_stats"), "cmd_stats missing"
    assert hasattr(mod, "cmd_memory"), "cmd_memory missing"
    assert hasattr(mod, "cmd_health"), "cmd_health missing"
    assert hasattr(mod, "cmd_cpu"), "cmd_cpu missing"
    assert hasattr(mod, "cmd_disk"), "cmd_disk missing"
    assert hasattr(mod, "cmd_gpu"), "cmd_gpu missing"
    assert hasattr(mod, "cmd_processes"), "cmd_processes missing"

