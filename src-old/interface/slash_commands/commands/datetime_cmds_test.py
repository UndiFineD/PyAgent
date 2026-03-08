# Auto-synced test for interface/slash_commands/commands/datetime_cmds.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "datetime_cmds.py"
    parts = list(p.with_suffix("").parts)
    if "src" in parts:
        idx = parts.index("src") + 1
        module_name = ".".join(parts[idx:])
    else:
        module_name = ".".join(parts)
    spec = importlib.util.spec_from_file_location(module_name, p)
    mod = importlib.util.module_from_spec(spec)
    import sys

    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "cmd_datetime"), "cmd_datetime missing"
    assert hasattr(mod, "cmd_date"), "cmd_date missing"
    assert hasattr(mod, "cmd_time"), "cmd_time missing"
    assert hasattr(mod, "cmd_uptime"), "cmd_uptime missing"
    assert hasattr(mod, "cmd_timestamp"), "cmd_timestamp missing"
