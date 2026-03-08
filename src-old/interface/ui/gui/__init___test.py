import importlib


def test_import_src_interface_ui_gui___init__():
    mod = importlib.import_module("src.interface.ui.gui.__init__")
    # Basic smoke tests
    assert mod is not None
