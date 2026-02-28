import importlib


def test_import_src_interface_ui_cli___init__():
    mod = importlib.import_module("src.interface.ui.cli.__init__")
    # Basic smoke tests
    assert mod is not None
