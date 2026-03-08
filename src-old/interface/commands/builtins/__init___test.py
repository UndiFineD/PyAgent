import importlib


def test_import_src_interface_commands_builtins___init__():
    mod = importlib.import_module("src.interface.commands.builtins.__init__")
    # Basic smoke tests
    assert mod is not None
