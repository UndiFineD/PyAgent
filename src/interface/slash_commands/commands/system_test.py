# Auto-synced test for interface/slash_commands/commands/system.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "system.py"
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
    assert hasattr(mod, "cmd_stats"), "cmd_stats missing"
    assert hasattr(mod, "cmd_memory"), "cmd_memory missing"
    assert hasattr(mod, "cmd_health"), "cmd_health missing"
    assert hasattr(mod, "cmd_cpu"), "cmd_cpu missing"
    assert hasattr(mod, "cmd_disk"), "cmd_disk missing"
    assert hasattr(mod, "cmd_gpu"), "cmd_gpu missing"
    assert hasattr(mod, "cmd_processes"), "cmd_processes missing"

