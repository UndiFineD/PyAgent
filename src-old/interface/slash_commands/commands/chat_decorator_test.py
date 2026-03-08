# Auto-synced test for interface/slash_commands/commands/chat_decorator.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "chat_decorator.py"
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
    assert hasattr(mod, "cmd_human"), "cmd_human missing"
    assert hasattr(mod, "cmd_ai"), "cmd_ai missing"
    assert hasattr(mod, "cmd_system_message"), "cmd_system_message missing"
    assert hasattr(mod, "cmd_thinking"), "cmd_thinking missing"
    assert hasattr(mod, "cmd_codeblock"), "cmd_codeblock missing"
    assert hasattr(mod, "cmd_chat"), "cmd_chat missing"
    assert hasattr(mod, "cmd_chat_theme"), "cmd_chat_theme missing"
    assert hasattr(mod, "cmd_chat_preview"), "cmd_chat_preview missing"
