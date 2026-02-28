# Auto-synced test for interface/slash_commands/commands/observability.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "observability.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "cmd_cache"), "cmd_cache missing"
    assert hasattr(mod, "cmd_counters"), "cmd_counters missing"
    assert hasattr(mod, "cmd_telemetry"), "cmd_telemetry missing"
    assert hasattr(mod, "cmd_logs"), "cmd_logs missing"

