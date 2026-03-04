# Auto-synced test for interface/slash_commands/api.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "api.py"
    # derive module name from path (everything under src)
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
    assert hasattr(mod, "get_slash_commands"), "get_slash_commands missing"
    assert hasattr(mod, "reset_slash_commands"), "reset_slash_commands missing"
    assert hasattr(mod, "process_prompt"), "process_prompt missing"
    assert hasattr(mod, "execute_command"), "execute_command missing"
    assert hasattr(mod, "get_help"), "get_help missing"

