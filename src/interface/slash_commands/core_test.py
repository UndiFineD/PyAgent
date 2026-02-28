# Auto-synced test for interface/slash_commands/core.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "core.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "CommandContext"), "CommandContext missing"
    assert hasattr(mod, "CommandResult"), "CommandResult missing"
    assert hasattr(mod, "CommandDefinition"), "CommandDefinition missing"
    assert hasattr(mod, "CommandRegistry"), "CommandRegistry missing"
    assert hasattr(mod, "ParsedCommand"), "ParsedCommand missing"
    assert hasattr(mod, "parse_commands"), "parse_commands missing"
    assert hasattr(mod, "ProcessedPrompt"), "ProcessedPrompt missing"
    assert hasattr(mod, "SlashCommands"), "SlashCommands missing"

