# Auto-synced test for interface/slash_commands/commands/datetime_cmds.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "datetime_cmds.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "cmd_datetime"), "cmd_datetime missing"
    assert hasattr(mod, "cmd_date"), "cmd_date missing"
    assert hasattr(mod, "cmd_time"), "cmd_time missing"
    assert hasattr(mod, "cmd_uptime"), "cmd_uptime missing"
    assert hasattr(mod, "cmd_timestamp"), "cmd_timestamp missing"

