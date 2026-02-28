# Auto-synced test for interface/slash_commands/commands/environment.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "environment.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "cmd_version"), "cmd_version missing"
    assert hasattr(mod, "cmd_env"), "cmd_env missing"
    assert hasattr(mod, "cmd_python"), "cmd_python missing"
    assert hasattr(mod, "cmd_cwd"), "cmd_cwd missing"
    assert hasattr(mod, "cmd_hostname"), "cmd_hostname missing"
    assert hasattr(mod, "cmd_user"), "cmd_user missing"
    assert hasattr(mod, "cmd_venv"), "cmd_venv missing"

