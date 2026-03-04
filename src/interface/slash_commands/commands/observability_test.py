# Auto-synced test for interface/slash_commands/commands/observability.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "observability.py"
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
    assert hasattr(mod, "cmd_cache"), "cmd_cache missing"
    assert hasattr(mod, "cmd_counters"), "cmd_counters missing"
    assert hasattr(mod, "cmd_telemetry"), "cmd_telemetry missing"
    assert hasattr(mod, "cmd_logs"), "cmd_logs missing"

