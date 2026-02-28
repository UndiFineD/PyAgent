# Auto-synced test for interface/slash_commands/commands/utility.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "utility.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "cmd_tokens"), "cmd_tokens missing"
    assert hasattr(mod, "cmd_uuid"), "cmd_uuid missing"
    assert hasattr(mod, "cmd_random"), "cmd_random missing"
    assert hasattr(mod, "cmd_choice"), "cmd_choice missing"
    assert hasattr(mod, "cmd_hash"), "cmd_hash missing"
    assert hasattr(mod, "cmd_base64"), "cmd_base64 missing"
    assert hasattr(mod, "cmd_length"), "cmd_length missing"
    assert hasattr(mod, "cmd_help"), "cmd_help missing"
    assert hasattr(mod, "cmd_echo"), "cmd_echo missing"
    assert hasattr(mod, "cmd_upper"), "cmd_upper missing"
    assert hasattr(mod, "cmd_lower"), "cmd_lower missing"

